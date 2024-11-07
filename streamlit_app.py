import streamlit as st
import fitz  # PyMuPDF
from model import *

st.title('Course Compass')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize resume text
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# File uploader for resume
uploaded_file = st.file_uploader("Upload any file like your resume (PDF)", type="pdf")

# Extract text from the uploaded PDF file
if uploaded_file and "uploaded_file" not in st.session_state:
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    resume_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        resume_text += page.get_text()
    st.session_state.resume_text = f"User's File to understand user's background: {resume_text}"
    st.session_state.uploaded_file = uploaded_file

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input for additional message
prompt = st.chat_input("What do you want to learn today?")

if prompt:
    user_message = prompt
    if st.session_state.resume_text:
        user_message = f"{st.session_state.resume_text}\n{prompt}"

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    print(user_message)
    response = get_response(user_message)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})