from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field


load_dotenv()

llm=ChatOpenAI(model_name="gpt-4.1",temperature=0,api_key="")

class MessageClassifier()
