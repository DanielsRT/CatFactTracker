from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import sqlite3
import random
from typing import List
import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>Cat Facts API is running. Try <a href='/catfacts'>/catfacts</a>.</h2>"

@app.get("/catfacts", response_model=List[dict])
def get_all_cat_facts():
    conn = db.setup_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cat_facts")
    rows = cursor.fetchall()
    conn.close()
    return [{"id" : row["id"], "fact": row["fact"], "created_at": row["created_at"]} for row in rows]

@app.get("/catfacts/random")
def get_random_cat_fact():
    conn = db.setup_database()
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM cat_facts")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="No cat facts available")
    return {"fact": random.choice(rows)["fact"]}

@app.post("/catfacts")
def add_cat_fact(fact: str = Form(...)):
    if not fact.strip():
        raise HTTPException(status_code=400, detail="Fact cannot be empty")
    conn = db.setup_database()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cat_facts (fact) VALUES (?)", (fact.strip(),))
        conn.commit()
        return {"message": "Cat fact added successfully."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Duplicate cat fact.")
    finally:
        conn.close()