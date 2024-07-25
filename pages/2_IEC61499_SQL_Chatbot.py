import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from SQL.sql_agent import create_custom_sql_agent
from langchain_core.messages import HumanMessage
    

# --- USER AUTHENTICATION ---
names = ["Midhun Xavier", "Sandeep Patil", "Valeriy Vyatkin"]
usernames = ["MX", "SP", "VV"]

# load hashed passwords
file_path = Path(__file__).parent / "../Authentication/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "QA_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status == True:
    st.title("📝 IEC 61499 Solution Q&A with AI")
    with st.sidebar:
        db_uri = st.text_input("Database connection string", key="db_uri", type="password")
        "example : postgresql+psycopg2://postgres:postgres@localhost:5432/HotWaterTank"
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if db_uri:
        agent = create_custom_sql_agent(f"postgresql+psycopg2://postgres:postgres@130.240.196.40:5432/HotWaterTank")

    if prompt := st.chat_input():
        if not db_uri:
                st.info("Please add your IEC 61499 Application Database connection string")
                st.stop()
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

    

        response =  agent.invoke({"input": prompt})
            
        st.session_state.messages.append({"role": "assistant", "content": response['output']})
        st.chat_message("assistant").write(response['output'])
