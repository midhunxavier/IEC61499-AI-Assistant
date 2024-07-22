import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from RAG.RAG_Graph import setup_workflow
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
    uploaded_file = st.file_uploader("Upload IEC 61499 Solution Zip folder", type=(".zip"))
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if uploaded_file:
        workflow = setup_workflow(uploaded_file)

    if prompt := st.chat_input():
        if not uploaded_file:
                st.info("Please add your IEC 61499 Application soloution ZIP")
                st.stop()
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

    

        response =  workflow.invoke({"messages": [HumanMessage(content=prompt)]},config={"configurable": {"thread_id": 42}})
            
        st.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
        st.chat_message("assistant").write(response["messages"][-1].content)
