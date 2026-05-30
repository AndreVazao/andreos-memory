import os
import json
import time
import sqlite3
from datetime import datetime

# Optional dependencies (graceful fallback)
try:
    from sentence_transformers import SentenceTransformer
    _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    EMBEDDING_MODE = "transformers"
except Exception:
    _embedder = None
    EMBEDDING_MODE = "none"

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    _tfidf = TfidfVectorizer()
    TFIDF_MODE = True
except Exception:
    _tfidf = None
    TFIDF_MODE = False

MEMORY_PATH = os.getenv("ANDREOS_MEMORY", r"C:\ProgramasGodmode\andreos-memory")
DB_PATH = os.path.join(MEMORY_PATH, "core_index.db")

# -----------------------------
# DB INIT
# -----------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT,
        content TEXT,
        embedding TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# EMBEDDINGS
# -----------------------------

def embed(text: str):
    if EMBEDDING_MODE == "transformers":
        vec = _embedder.encode(text)
        return json.dumps(vec.tolist())

    if TFIDF_MODE:
        vec = _tfidf.fit_transform([text]).toarray()[0]
        return json.dumps(vec.tolist())

    # fallback raw hash vector
    return json.dumps([hash(text) % 1000])

# -----------------------------
# INDEXING
# -----------------------------

def index_file(file_path: str):
    try:
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if len(content.strip()) == 0:
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        embedding = embed(content)
        timestamp = datetime.utcnow().isoformat()

        c.execute("""
            INSERT INTO memory (path, content, embedding, timestamp)
            VALUES (?, ?, ?, ?)
        """, (file_path, content[:5000], embedding, timestamp))

        conn.commit()
        conn.close()

        print(f"[INDEX] Indexed: {file_path}")

    except Exception as e:
        print(f"[INDEX ERROR] {file_path} -> {e}")

# -----------------------------
# SEARCH
# -----------------------------

def search_memory(query: str, limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT path, content, timestamp FROM memory")
    rows = c.fetchall()

    conn.close()

    results = []
    for path, content, ts in rows:
        score = 0

        # simple scoring (upgrade point)
        for token in query.lower().split():
            if token in content.lower():
                score += 1

        if score > 0:
            results.append((score, path, ts, content[:300]))

    results.sort(reverse=True, key=lambda x: x[0])

    return results[:limit]

# -----------------------------
# BOOT
# -----------------------------

if __name__ == "__main__":
    print("[MEMORY INDEX] Initializing...")
    init_db()
    print(f"[MEMORY INDEX] Mode: {EMBEDDING_MODE}")
    print(f"[MEMORY INDEX] DB: {DB_PATH}")