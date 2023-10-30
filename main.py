import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from streamlit_option_menu import option_menu
from loader import Load
from extract import tool_creation, call_agent
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
import time

import dotenv
dotenv.load_dotenv()

st.set_page_config(layout='wide')

st.title('Resume Evaluator and Upskill Recommender')

col1, col2 = st.columns([2,1])

if 'api_results' not in st.session_state:
    st.session_state.api_results = ""

chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

if 'resume_data' not in st.session_state:
    st.session_state.resume_data = ""


if 'is_file_uploaded' not in st.session_state:
    st.session_state.is_file_uploaded = False

if 'resume_file_name' not in st.session_state:
    st.session_state.resume_file_name = ""

with st.sidebar:
    selected = option_menu(
        menu_title="Chats",
        options=['Resume Evaluator', 'Chat']
    )

if selected == 'Chat':
    if 'messages' not in st.session_state:
        st.session_state.messages = [
        SystemMessage(content=f"You are a resume parser. \n This is a resume.\n {st.session_state.resume_data} \n Answer the following questions using the resume given above. Don't add any new information that is not present in the resume.")
    ]
    if not st.session_state.is_file_uploaded:
        st.write('Upload your resume first to enable the chat feature!')
    else:
        user_input = st.text_input("Enter your question here:", key="user_input")
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner('Thinking...'):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                message(msg.content, is_user=True, key=str(i)+'_user')
            else:
                message(msg.content, is_user=False, key=str(i)+'_ai')

elif selected == "Resume Evaluator":
    uploaded_file=""
    with col2:
        if not st.session_state.is_file_uploaded:
            uploaded_file = st.file_uploader("Upload your Resume here")
            l = Load()
            if uploaded_file:
                st.session_state.resume_file_name = uploaded_file.name
                st.session_state.resume_data = l.identify_and_load(st.session_state.resume_file_name)
                st.session_state.is_file_uploaded = True
        else:
            st.write(f"Your resume, {st.session_state.resume_file_name} is uploaded successfully")
        with st.form('job_descrption'):
            txt = st.text_area("Enter your Job Descrption here")
            submitted = st.form_submit_button('Evaluate')
            if submitted and txt != "" and uploaded_file is not None:
                tool_creation("resume", st.session_state.resume_data)
                tool_creation("job_description", txt)
                st.write('Calling API...')
                out = call_agent("Are the skills in job description and resume matching?")
                st.session_state.api_results = out["output"]
            elif submitted and not uploaded_file:
                st.write('No file uploaded! Please upload the file!')
            elif submitted and txt == "":
                st.write('Job description is empty! Please enter the job description!')

    with col1:
        if st.session_state.api_results == "":
            st.write('Your evaluation results will be displayed here')
        else:
            st.write(st.session_state.api_results)
