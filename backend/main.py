from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .rag_logic import chunk_text
from .rag_logic import retrieve_top_k_contexts
from .rag_logic import build_prompt
from .rag_logic import generate_answer

app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/ask")
async def ask(request: Request):
    data = await request.json()

    context = data["context"]
    question = data["question"]

    # context to chunks for retrival
    chunk_text(context)

    # retrival of context 
    reference = retrieve_top_k_contexts(question,3)

    # prompt 
    prompt = build_prompt(question,reference)

    # generate answer
    answer = generate_answer(prompt)

    return { "context": reference , "answer": answer}