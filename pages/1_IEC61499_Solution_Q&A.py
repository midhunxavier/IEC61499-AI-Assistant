import streamlit as st_qa
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  
from RAG.RAG_Graph import setup_workflow
from langchain_core.messages import HumanMessage
    

names = ["Midhun Xavier", "Sandeep Patil", "Valeriy Vyatkin"]
usernames = ["MX", "SP", "VV"]

file_path = Path(__file__).parent / "../Authentication/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "QA_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st_qa.error("Username/password is incorrect")

if authentication_status == None:
    st_qa.warning("Please enter your username and password")

if authentication_status == True:
    st_qa.title("📝 IEC 61499 Solution Q&A with AI")
    uploaded_file = st_qa.file_uploader("Upload IEC 61499 Solution Zip folder", type=(".zip"))
    if "messages" not in st_qa.session_state:
        st_qa.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st_qa.session_state.messages:
        st_qa.chat_message(msg["role"]).write(msg["content"])

    if uploaded_file:
        workflow = setup_workflow(uploaded_file)

    if prompt := st_qa.chat_input():
        if not uploaded_file:
                st_qa.info("Please add your IEC 61499 Application soloution ZIP")
                st_qa.stop()
        
        st_qa.session_state.messages.append({"role": "user", "content": prompt})
        st_qa.chat_message("user").write(prompt)

    

        response =  workflow.invoke({"messages": [HumanMessage(content=prompt)]},config={"configurable": {"thread_id": 42}})
            
        st_qa.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
        st_qa.chat_message("assistant").write(response["messages"][-1].content)
