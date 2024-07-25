from SQL.database_conn import get_database_connection
from SQL.llm_setup import get_llm, get_prompt_template
from SQL.utility import query_as_list
from SQL.retriever_setup import get_retriever_tool
from langchain.agents.agent_toolkits import create_sql_agent

def create_custom_sql_agent(db_uri):
    db = get_database_connection(db_uri)

    variables = query_as_list(db, "SELECT \"Path\" FROM public.\"ArchiveInstances\";")


    prompt_template = get_prompt_template()

    retriever_tool = get_retriever_tool(variables)

    llm = get_llm()

    agent = create_sql_agent(
        llm=llm,
        db=db,
        extra_tools=[retriever_tool],
        prompt=prompt_template,
        agent_type="openai-tools",
        verbose=False,
    )

    return agent
