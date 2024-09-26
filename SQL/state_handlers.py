
from SQL.tools import (
    search_proper_names_tool, 
    get_variable_details_tool, 
    get_relevant_table_schema_tool, 
    db_query_tool
    )

from langgraph.graph.message import AnyMessage, add_messages
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage

from typing import List, TypedDict, Optional, Annotated, Dict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph import END, StateGraph, START

class SqlInfoState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def should_continue(state: SqlInfoState) -> Literal["db_query_tool", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "db_query_tool"
    return "__end__"



system = """  You are an assistant in identifying the exact variable name from the user question using search_proper_name_tool.              
              """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_proper_names_model = system_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([search_proper_names_tool])

def search_proper_names(state: SqlInfoState):
    response =search_proper_names_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}

system = """  You are an expert in identifying the variable's details using  get_variable_details_tool.
              """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_variable_info_model = system_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([get_variable_details_tool])

def search_variable_info(state: SqlInfoState):
    response =search_variable_info_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}
    
system = """  You are an expert in identifying the  variable's table schema using the get_relevant_table_schema_tool.
         """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_table_info_model = system_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([get_relevant_table_schema_tool])

def search_table_info(state: SqlInfoState):
    response =search_table_info_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}



query_gen_system = """You are a SQL expert with a strong attention to detail.

Given an input question, generate a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer.

DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.

When generating the query:

1. Output the SQL query that answers the input question without a tool call.
2. Unless the user specifies a specific number of examples, limit your query to at most 5 results.
3. Order the results by a relevant column to return the most interesting examples in the database.
4. Only query for the relevant columns given the question; do not select all columns from a table.

Error Handling:

1. If you get an error while executing a query, rewrite the query and try again.
2. If you get an empty result set, rewrite the query to obtain a non-empty result set.
3. Never fabricate information if there is not enough data to answer the question.

Restrictions:
Do not make any DML statements (INSERT, UPDATE, DELETE, DROP, etc.) to the database.

Guidance for Information Retrieval:

Use the  archiveId which is similar to the extracted instanceId of the variable to generate SQL query.
Use the provided table_schema for according to its  to construct the query.
Ensure that extracted archiveId matches only the last 5 digits in the archveId column in a given schema.

Once identified the query then execute the query using db_query_tool tool to get the answer. 

"""
query_gen_prompt = ChatPromptTemplate.from_messages(
    [("system", query_gen_system), ("placeholder", "{messages}")]
)
query_gen_model = query_gen_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([db_query_tool])

def search_query_info(state: SqlInfoState):
    response =query_gen_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}
       

