# 🎥 ChatWithYT

**ChatWithYT** is an AI-powered chatbot that lets you talk to any YouTube video using its transcript. Instead of watching the whole video, just paste the video URL and ask your questions — the bot will respond with accurate, transcript-based answers using powerful language models.

---

## ✨ Features

- 🔗 Input any YouTube video URL
- 🧠 Ask questions and get smart, relevant answers
- 📄 Uses actual video transcript (no hallucinated info)
- ✍️ Summarize or extract key points
- 💬 Clean chatbot-style UI with chat history
- ⚡ Powered by LangChain, Google Gemini, and Hugging Face Embeddings

---

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **LLM Framework**: LangChain
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: FAISS
- **Transcript Source**: YouTube Transcript API
- **LLM**: Gemini 1.5 Flash via `langchain-google-genai`

---

## 🚀 How It Works

1. You paste a YouTube video URL.
2. The transcript is fetched using `YouTubeTranscriptApi`.
3. Transcript is split into chunks.
4. Embeddings are generated and stored using FAISS.
5. LangChain retrieves relevant transcript chunks using similarity search.
6. Gemini generates an answer based on the retrieved transcript parts.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/chatwithyt.git
cd chatwithyt


ArchitecTure
<img width="1838" height="538" alt="image" src="https://github.com/user-attachments/assets/7a1b5d44-40c9-4570-8386-34c4a88b3f60" />

