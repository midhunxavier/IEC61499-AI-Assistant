from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


def get_prompt_template():
    
    examples = [
        {"input": "List all variable Names.", "query": "SELECT \"Path\" FROM public.\"ArchiveInstances;"},
        {
            "input": "Find the instance id for ECC_STATE.",
            "query": "SELECT \"InstanceId\" FROM public.\"ArchiveInstances\" WHERE \"Path\" LIKE '%ECC_STATE%';",
        },
        {
            "input": "Find the Latest value of ECC State and its timestamp at which the action occured",
            "query":  "SELECT t2.\"TimeStamp\", t2.\"Value\" FROM public.\"ArchiveInstances\" t1 JOIN public.\"StringValues\" t2 ON (t1.\"InstanceId\" = t2.\"ArchiveId\") WHERE \"Path\" LIKE \'%ECC_STATE%\' ORDER BY t2.\"TimeStamp\" DESC LIMIT 1; ;",
        },
        {
            "input": "Whether tank is ruptured?",
            "query":  "SELECT  t2.\"Value\" FROM public.\"ArchiveInstances\" t1 JOIN public.\"BoolValues\" t2 ON (t1.\"InstanceId\" = t2.\"ArchiveId\") WHERE \"Path\" LIKE \'%TankRupture%\' ORDER BY t2.\"TimeStamp\" DESC LIMIT 1; ;",
        },
        {
            "input": "What is the Water slider values between start time stamp and end time stamp",
            "query":  "SELECT  * FROM public.\"ArchiveInstances\" t1 JOIN public.\"RealValues\" t2 ON (t1.\"InstanceId\" = t2.\"ArchiveId\") WHERE (\"Path\" LIKE '%WaterLevelSlider') AND (t2.\"TimeStamp\" BETWEEN '2024-04-24 14:56:43.382266' AND '2024-04-24 15:00:02.047399')",
        },
    ]


    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )
   
    system_prefix = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool! 

    You have access to the following tables: {table_names}

    If the question does not seem related to the database, just return "I don't know" as the answer.

    Database Information:

    There are many tables in the database. AlarmInstances, Alarm Lines tables are irrelevant so dont use it.
    ArchiveInstance is the important table it helps to identify the Instance Id of variable and then its used to find the values of variable from other tables.
    There are different tables according to its data types String, Bool, Real, Int etc. Each Data type has a table associated with it. 
    Example1 : String data type has a StringValues table.  consider only StringValues table and  ignore other tables like StringValuesXXXXXX.
    Example2 : Bool data type has a BoolValues table.  consider only BoolValues table and  ignore other tables like BoolValuesXXXXXX.


    Information retreival guidance

            Example Query 1
            Query = Find the latest values of any variable. (for example we can consider variable is ECC STATE )
            First identify the Instance Id of variable from ArchiveInstance table and its datatype  i,e : 5423300058043615869 is instance id  and  String is datatype for ECC STATE variable.
            According to datatype, go the StringValue table  match the ArchiveId with InstanceId. (Note: It maches only the last 5 digits).
            Finally according to descending order of timestamp identify the value fron String value table.

    Here are some examples of user inputs and their corresponding SQL queries:

    """

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input} \n SQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("system", system_prefix), ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
