# main.py

import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


def load_transcript(url: str) -> str | None:
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    if match:
        try:
            video_id = match.group(1)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            return " ".join(chunk["text"] for chunk in transcript_list)
        except TranscriptsDisabled:
            return None
    return None


def text_splitter(transcript):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([transcript])


def generate_embeddings(chunks):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return FAISS.from_documents(chunks, embeddings)


def retriever_docs(vector_store):
    return vector_store.as_retriever(search_type='similarity', search_kwargs={"k": 3})


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


def generation_chain(retriever):
    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
        input_variables=['context', 'question']
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    return parallel_chain | prompt | llm | StrOutputParser()
