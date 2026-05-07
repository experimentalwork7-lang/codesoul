import sqlite3
import json

def init_memory():
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE,
            value TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            description TEXT,
            language TEXT
        )
    """)
    conn.commit()
    conn.close()

def save(key, value):
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)",
              (key, json.dumps(value)))
    conn.commit()
    conn.close()

def load(key):
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None

def save_project(name, description, language):
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO projects (name, description, language) VALUES (?, ?, ?)",
              (name, description, language))
    conn.commit()
    conn.close()

def get_projects():
    conn = sqlite3.connect("codesoul_memory.db")
    c = conn.cursor()
    c.execute("SELECT name, description, language FROM projects")
    rows = c.fetchall()
    conn.close()
    return rows