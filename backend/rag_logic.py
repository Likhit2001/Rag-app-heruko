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

bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

llm_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


def chunk_text(context_text: str, chunk_size: int = 300):
   
    chunk_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    os.makedirs("chunk_store", exist_ok=True)

    # Split the input string into smaller chunks
    chunks = textwrap.wrap(context_text, width=chunk_size, break_long_words=False)
    chunk_text_to_original = [context_text] * len(chunks)

    # Encode chunks in batches
    batch_size = 32
    context_embeddings = []
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i + batch_size]
        emb = chunk_model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        context_embeddings.append(emb)

    context_embeddings = np.vstack(context_embeddings)

    # Save FAISS index
    dimension = context_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(context_embeddings)
    faiss.write_index(index, "chunk_store/context_index.faiss")

    # Save mapping to retrieve text later
    pd.DataFrame({
        "chunk": chunks,
        "original_context": chunk_text_to_original
    }).to_csv("chunk_store/context_mapping.csv", index=False)

    print("FAISS index and chunk mapping saved to 'chunk_store/'")

def retrieve_top_k_contexts(question, k=5):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))


    base_dir = os.path.dirname(os.path.abspath(__file__))
    retrieve_model = SentenceTransformer(os.path.join(project_root, "final_model_partial_frezzing"))

    index = faiss.read_index(os.path.join(project_root, "chunk_store", "context_index.faiss"))
    context_df = pd.read_csv(os.path.join(project_root, "chunk_store", "context_mapping.csv"))

    retrieve_model.eval()

    query_vec = retrieve_model.encode([question], convert_to_numpy=True)
    query_vec = np.expand_dims(query_vec, axis=0) if query_vec.ndim == 1 else query_vec

    _, indices = index.search(query_vec, k)
    
    retrieved_contexts = [context_df.iloc[i]["chunk"] for i in indices[0]]
    return retrieved_contexts

def build_prompt(question, contexts):
    prompt = f"Answer the following question using complete sentences based only on the given context.\n"
    prompt += "\n".join(contexts)
    prompt += f"\n\nQuestion: {question}\nAnswer:"
    return prompt


from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model_generation = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model_generation.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# uvicorn backend.main:app --reload  




