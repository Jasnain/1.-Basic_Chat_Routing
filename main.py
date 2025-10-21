import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_mesages
from langchain.chat_models import ChatOpenAI
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
    messages: Annotated[list,add_mesages]
    messages_type: str| None

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
    