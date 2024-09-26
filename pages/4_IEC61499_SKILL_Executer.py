import streamlit as st_skill
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  
from SKILL_EXE.skill_exe import set_react_skill_graph
from langchain_core.messages import HumanMessage
    

names = ["Midhun Xavier", "Sandeep Patil", "Valeriy Vyatkin"]
usernames = ["MX", "SP", "VV"]

file_path = Path(__file__).parent / "../Authentication/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "QA_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st_skill.error("Username/password is incorrect")

if authentication_status == None:
    st_skill.warning("Please enter your username and password")

if authentication_status == True:
    st_skill.title("📝 IEC 61499 SKILL EXEECUTER AI ASSISTANT")
    if "messages" not in st_skill.session_state:
        st_skill.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st_skill.session_state.messages:
        st_skill.chat_message(msg["role"]).write(msg["content"])

    workflow = set_react_skill_graph()

    if prompt := st_skill.chat_input():
        st_skill.session_state.messages.append({"role": "user", "content": prompt})
        st_skill.chat_message("user").write(prompt)

    



        for event in workflow.stream({"messages": ("user", prompt)}):
            for value in event.values():
                st_skill.session_state.messages.append({"role": "assistant", "content": value["messages"][-1].content})
                st_skill.chat_message("assistant").write(value["messages"][-1].content)
