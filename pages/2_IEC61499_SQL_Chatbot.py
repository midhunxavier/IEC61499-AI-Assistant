import streamlit as st_sql
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  
from SQL.graph_builder import create_sql_graph
from langchain_core.messages import HumanMessage


names = ["Midhun Xavier", "Sandeep Patil", "Valeriy Vyatkin"]
usernames = ["MX", "SP", "VV"]

file_path = Path(__file__).parent / "../Authentication/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "QA_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st_sql.error("Username/password is incorrect")

if authentication_status == None:
    st_sql.warning("Please enter your username and password")

if authentication_status == True:
    st_sql.title("📝 IEC 61499 Solution Q&A with AI")
    with st_sql.sidebar:
        db_uri = st_sql.text_input("Database connection string", key="db_uri", type="password")
        "example : postgresql+psycopg2://postgres:postgres@localhost:5432/HotWaterTank"
    if "messages" not in st_sql.session_state:
        st_sql.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st_sql.session_state.messages:
        st_sql.chat_message(msg["role"]).write(msg["content"])

    if db_uri:
        graph = create_sql_graph()

    if prompt := st_sql.chat_input():
        if not db_uri:
                st_sql.info("Please add your IEC 61499 Application Database connection string")
                st_sql.stop()
        
        st_sql.session_state.messages.append({"role": "user", "content": prompt})
        st_sql.chat_message("user").write(prompt)

        response =  graph.invoke({"messages": [HumanMessage(content=prompt)]})
            
        st_sql.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
        st_sql.chat_message("assistant").write(response["messages"][-1].content)


