import os
import json
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def init_rag():
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS codebase (
            id INTEGER PRIMARY KEY,
            filepath TEXT UNIQUE,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def index_file(filepath):
    if not os.path.exists(filepath):
        return f"File '{filepath}' not found."
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO codebase (filepath, content) VALUES (?, ?)",
              (filepath, content))
    conn.commit()
    conn.close()
    return f"Indexed '{filepath}' successfully."

def search_codebase(query, top_k=2):
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("SELECT filepath, content FROM codebase")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return []
    contents = [r[1] for r in rows]
    filepaths = [r[0] for r in rows]
    vectorizer = TfidfVectorizer()
    all_texts = contents + [query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    query_vec = tfidf_matrix[-1]
    doc_vecs = tfidf_matrix[:-1]
    scores = cosine_similarity(query_vec, doc_vecs)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_indices:
        results.append((scores[i], filepaths[i], contents[i]))
    return results