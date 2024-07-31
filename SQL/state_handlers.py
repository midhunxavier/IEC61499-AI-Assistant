from langgraph.graph.message import AnyMessage, add_messages
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from SQL.tools import (
    search_proper_names_tool, 
    get_variable_details_tool, 
    get_relevant_table_schema_tool, 
    db_query_tool
    )

from typing import List, TypedDict, Optional, Annotated, Dict
from langgraph.graph.message import AnyMessage, add_messages

class SqlInfoState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def should_continue_search_proper_names(state: SqlInfoState) -> Literal["search_proper_names_tool", "search_variable_info", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "search_proper_names_tool"
    if "Hi" in last_message.content:
        return "__end__"
    return "search_variable_info"

def should_continue_search_variable_info(state: SqlInfoState) -> Literal["get_variable_details_tool", "search_table_info"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "get_variable_details_tool"
    return "search_table_info"

def should_continue_search_table_info(state: SqlInfoState) -> Literal["get_relevant_table_schema_tool", "search_query_info"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "get_relevant_table_schema_tool"
    return "search_query_info"

def should_continue_search_query_info(state: SqlInfoState) -> Literal["db_query_tool", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "db_query_tool"
    return "__end__"



system = """  You are an expert in identifying the different variable names from the user question. 
              The actual names in the similar in database is identified by executing the search_proper_names_tool.
              Example : 
              If the user mentions 3 different variable names then execute the search_proper_names_tool one variable at a time.

              If the query is a greeting then respond with "Hi"
              """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_proper_names_model = system_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([search_proper_names_tool])

def search_proper_names(state: SqlInfoState):
    response =search_proper_names_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}

system = """  You are an expert in identifying the different  variable's details from the extracted variable name from the database. 
              The variable information is identified by executing the get_variable_details_tool.
              Example : 
              If we have different variable names then execute the get_variable_details_tool one variable at a time to get the information.
              """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_variable_info_model = system_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([get_variable_details_tool])

def search_variable_info(state: SqlInfoState):
    response =search_variable_info_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}
    
system = """  You are an expert in identifying the different  variable's table schema from the extracted variable's ioType. 
              The variable information is identified by executing the get_relevant_table_schema_tool.
              Example : 
              If we have different variable names then execute the get_relevant_table_schema_tool using its ioType one variable at a time to get the information.
              """
system_prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("placeholder", "{messages}")]
)
search_table_info_model = system_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([get_relevant_table_schema_tool])

def search_table_info(state: SqlInfoState):
    response =search_table_info_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}

query_gen_system = """You are a SQL expert with a strong attention to detail.

Given an input question, generate a syntactically correct PostgreSQL query to retrieve the relevant data. Then look at the results of the query and return the answer.

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


Once identified the query then execute the query using execute_query tool to get the answer. 
"""
query_gen_prompt = ChatPromptTemplate.from_messages(
    [("system", query_gen_system), ("placeholder", "{messages}")]
)
query_gen_model = query_gen_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([db_query_tool])

def search_query_info(state: SqlInfoState):
    response =query_gen_model.invoke({"messages": state["messages"]})
    if response:
        return {"messages": [response]}
    else:
        return {"messages": [{"role": "ai", "content":  "error occurred"}]}
        
