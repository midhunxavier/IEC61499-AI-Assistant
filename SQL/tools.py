from langchain_community.utilities import SQLDatabase
from typing import Any
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langgraph.prebuilt import ToolNode
import ast
import re
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI


db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:postgres@localhost:5432/HotWaterTank")


def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    """
    Create a ToolNode with a fallback to handle errors and surface them to the agent.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))


variables = query_as_list(db, """ SELECT "Path" FROM public."ArchiveInstances"; """)
vector_db = FAISS.from_texts(variables , OpenAIEmbeddings())
retriever = vector_db.as_retriever(search_kwargs={"k": 1})

@tool
def search_proper_names_tool(query: str) -> str:
    """ Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is valid proper noun.
    """
    try:
        result = retriever.invoke(query)
        return result
    except Exception as e:
        return "Error: Cannot find the proper noun."
    

@tool
def get_variable_details_tool(variable_name: str) -> str:
    """ Use to look up a variable's information from the database. 
        
        Input is an extracted variable name from the database, 
        output is a variable's details
            "path".
            "instanceId"
            "ioType" 
    """
    query = """ SELECT "Path", "InstanceId", "IOType" FROM public."ArchiveInstances" WHERE "Path" LIKE '%{0}%';""".format(variable_name)
    result = db.run_no_throw(query)
    if not result:
        return  "Error: Cannot retrieve the variable information"
    else:
        return result


toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(model="gpt-4o-mini"))
tools = toolkit.get_tools()
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

@tool
def get_relevant_table_schema_tool(ioType: str) -> str:
    """ Use to look up a variable's table schema from the database. 
        Input is an ioType value variable.
        output is a table schema of the variable from database
    """
    try:
        TableName = ioType[0].upper() + ioType[1:].lower()+"Values"
        table_schema = get_schema_tool.invoke(TableName)
        return table_schema
    except Exception as e:
        return "Error: Cannot find the relevant table schema."
    

@tool
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return  result