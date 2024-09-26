import streamlit as st_viz
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  
from DATA_VIZ.graph_builder import create_sql_graph
from langchain_core.messages import HumanMessage
import os

names = ["Midhun Xavier", "Sandeep Patil", "Valeriy Vyatkin"]
usernames = ["MX", "SP", "VV"]

file_path = Path(__file__).parent / "../Authentication/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "QA_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st_viz.error("Username/password is incorrect")

if authentication_status == None:
    st_viz.warning("Please enter your username and password")

if authentication_status == True:
    st_viz.title("📝 IEC 61499 Data Visualizer App")
    with st_viz.sidebar:
        db_uri = st_viz.text_input("Database connection string", key="db_uri", type="password")
        "example : postgresql+psycopg2://postgres:postgres@localhost:5432/HotWaterTank"
    if "messages" not in st_viz.session_state:
        st_viz.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st_viz.session_state.messages:
        st_viz.chat_message(msg["role"]).write(msg["content"])

    if db_uri:
        graph = create_sql_graph()

    if os.path.exists("temp.png"):
        os.remove("temp.png")
    if prompt := st_viz.chat_input():
        if not db_uri:
                st_viz.info("Please add your IEC 61499 Application Database connection string")
                st_viz.stop()
        
        st_viz.session_state.messages.append({"role": "user", "content": prompt})
        st_viz.chat_message("user").write(prompt)


        

        response =  graph.invoke({"messages": [HumanMessage(content=prompt)]})
            
        st_viz.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
        st_viz.chat_message("assistant").write(response["messages"][-1].content)
        if os.path.exists("temp.png"):
            st_viz.image("temp.png") 