from langchain_community.utilities import SQLDatabase

def get_database_connection(db_uri):
    return SQLDatabase.from_uri(db_uri)

