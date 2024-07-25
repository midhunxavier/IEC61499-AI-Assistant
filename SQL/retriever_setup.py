from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def get_retriever_tool(variables):
    vector_db = FAISS.from_texts(variables, OpenAIEmbeddings())
    retriever = vector_db.as_retriever(search_kwargs={"k": 1})
    description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
    valid proper nouns. Use the noun most similar to the search."""
    return create_retriever_tool(
        retriever,
        name="search_proper_nouns",
        description=description,
    )