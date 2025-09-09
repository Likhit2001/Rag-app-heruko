import torch
from transformers import (
    BertTokenizer, BertModel,
    AutoTokenizer, AutoModelForSeq2SeqLM
)
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import pandas as pd
import faiss
import os
from tqdm import tqdm
import textwrap
from pathlib import Path


tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model_generation = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

# Load embedding model once
base_dir = Path(__file__).resolve().parent.parent
model_path = base_dir / "final_model_partial_frezzing"
embedding_model = SentenceTransformer(str(model_path))

def chunk_text(context_text: str, chunk_size: int = 300):
    chunks = textwrap.wrap(context_text, width=chunk_size, break_long_words=False)
    chunk_text_to_original = [context_text] * len(chunks)

    batch_size = 32
    context_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        emb = embedding_model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        context_embeddings.append(emb)

    context_embeddings = np.vstack(context_embeddings)

    dimension = context_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(context_embeddings)

    return index, pd.DataFrame({
        "chunk": chunks,
        "original_context": chunk_text_to_original
    })

def retrieve_top_k_contexts(question, context_paragraph, k=5):
    index, context_df = chunk_text(context_paragraph)

    base_dir = Path(__file__).resolve().parent.parent
    model_path = base_dir / "final_model_partial_frezzing"

    retrieve_model = SentenceTransformer(str(model_path))
    retrieve_model.eval()

    query_vec = retrieve_model.encode([question], convert_to_numpy=True)
    query_vec = np.expand_dims(query_vec, axis=0) if query_vec.ndim == 1 else query_vec

    _, indices = index.search(query_vec, k)
    retrieved_contexts = [context_df.iloc[i]["chunk"] for i in indices[0]]

    return retrieved_contexts

def build_prompt(question, contexts):
    prompt = "Answer the following question using complete sentences based only on the given context.\n"
    prompt += "\n".join(contexts)
    prompt += f"\n\nQuestion: {question}\nAnswer:"
    return prompt

def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model_generation.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
