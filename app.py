# app.py

import streamlit as st
from main import (
    load_transcript,
    text_splitter,
    generate_embeddings,
    retriever_docs,
    generation_chain,
)
from dotenv import load_dotenv
load_dotenv()

# --- Session state initialization ---
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_chain" not in st.session_state:
    st.session_state.chat_chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar for URL input ---
st.sidebar.title("YouTube Video")
url = st.sidebar.text_input("Enter YouTube Video URL:")
if st.sidebar.button("Load Transcript"):
    st.video(url)
    transcript = load_transcript(url)
    if transcript:
        chunks = text_splitter(transcript)
        st.session_state.vector_store = generate_embeddings(chunks)
        st.session_state.retriever = retriever_docs(st.session_state.vector_store)
        st.session_state.chat_chain = generation_chain(st.session_state.retriever)
        st.success("✅ Transcript loaded and chatbot is ready!")
    else:
        st.error("❌ Could not load transcript.")

# --- Main Chat UI ---
st.title("🎥 YouTube ChatBot")

if st.session_state.retriever:

    # Show history of Chats
    for msg in st.session_state.messages:
       # st.write("---____------____-----____")
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    user_input = st.chat_input("Ask a question about the video:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = st.session_state.chat_chain.invoke(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})