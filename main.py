import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(model_name="gpt-4.1",temperature=0,api_key=api_key)

class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"]= Field(
        ..., description="The type of message: 'emotional' or 'logical'"
    )

class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str| None

def classify_message(state:State):
    last_message= state["messages"][-1]
    classifier_llm=llm.with_structured_output(MessageClassifier)

    result=classifier_llm.invoke([
        {
            "role":"system",
            "content":"""
             Classify the user message as either:
             - 'emotional': if it asks for emotional support, therapy, guidance or has human feelings attached to it.
             - 'logical': if it requests factual information, data, or logical reasoning."""


        },
        {
            "role":"user",
            "content": last_message.content
        }
    ])
    return {"message_type": result.message_type}

def router(state: State):
    message_type= state.get("message_type","logical")
    if message_type=="emotional":
        return {"next": "therapist"}
    else:
        return {"next": "logical"}
    
def therapist_agent(state: State):
    last_message= state["messages"][-1]

    messages=[
        {   
            "role":"system",
            "content": """

                       You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
        },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply=llm.invoke(messages)
    return {"messages": [reply]}

def logical_agent(state: State):
    last_message= state["messages"][-1]

    messages=[
        {   
            "role":"system",
            "content": """

                       You are a logical assistant. Focus on providing factual information, data, and logical reasoning.
                        Analyze the user's message objectively and provide clear, concise answers.
                        Avoid delving into emotional aspects unless explicitly asked."""
        },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply=llm.invoke(messages)
    return {"messages": [reply]}   

graph_builder= StateGraph(State)

graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)

graph_builder.add_edge(START,"classify_message")
graph_builder.add_edge("classify_message","router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist":"therapist","logical":"logical"}
)

graph_builder.add_edge("therapist",END)
graph_builder.add_edge("logical",END)

graph=graph_builder.compile()

def run_chat():
    state= {"messages":[],"message_type": None}

    while True:
        user_input= input("Messahe: ")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting chat.")
            break

        state["messages"]= state.get("messages",[])+ [{"role":"user","content": user_input}]
        state= graph.invoke(state)

        if state.get("messages") and len(state["messages"])>0:
            last_message= state["messages"][-1]
            print(f"Assistant: {last_message.content}")

if __name__=="__main__":
    run_chat()

