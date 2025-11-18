
# 🔍 RAG-Powered QA System

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that combines dense retrieval using SentenceTransformers with generative response modeling using FLAN-T5. It enables users to ask questions and get precise, contextually rich answers based on retrieved documents.

[App Screenshot]![image](https://github.com/user-attachments/assets/b8582a4b-b71b-4066-80e9-bb2c3a14ab6e)


## 🚀 Live Demo

🔗 **Heroku App:** NOT HOSTED AS OF NOW

## 🚀  System Architecture
<img width="793" height="590" alt="Screenshot 2025-11-17 at 10 20 35 PM" src="https://github.com/user-attachments/assets/8505de79-27e4-4dfb-bfdc-7b8b3a99265d" />




## 📁 Project Structure

```
.
├── backend
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── rag_logic.py          # Core RAG logic (retriever + generator)
│   └── requirements.txt      # Backend Python dependencies
│
├── frontend
│   ├── app.py                # Streamlit frontend
│   ├── Dockerfile            # Dockerfile for frontend deployment
│   └── requirements.txt      # Frontend Python dependencies
│
├── chunk_store
│   └── 1.py                  # Code related to document chunking
│
├── final_model_partial_frezzing/
│                              # Folder for fine-tuned FLAN-T5 model
│
├── .github
│   └── workflows
│       └── main.yaml         # GitHub Actions CI/CD pipeline
```

## 🧠 Core Features

- **Dense Retrieval**: Semantic search via SentenceTransformers + FAISS.
- **Two-Stage Retrieval**: Topic-based clustering → deep retrieval only on relevant shards
- **Generative QA**: Uses FLAN-T5 to generate answers based on top-k context.
- **Modular Pipeline**: Decoupled backend (FastAPI) and frontend (Streamlit).
- **Containerized**: Fully Dockerized for ease of deployment.
- **CI/CD**: Automated builds and deployments using GitHub Actions.

## ⚙️ Technologies Used

- Python, FastAPI, Streamlit
- SentenceTransformers
- Hugging Face Transformers (FLAN-T5)
- FAISS
- Docker, Heroku
- GitHub Actions

## 📦 Deployment

```bash
# Build and run locally using Docker Compose
docker-compose up --build
```

To deploy on Heroku:

1. Push to GitHub
2. Connect GitHub repo to Heroku (for each service or monorepo)
3. Ensure Heroku Stack is set (e.g. `heroku stack:set container`)
4. Deploy via Heroku or CI/CD

---

📬 For questions or suggestions, feel free to open an issue or reach out!

