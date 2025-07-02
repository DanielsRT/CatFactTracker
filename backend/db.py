import sqlite3

DB_NAME = 'cat_facts.db'

def setup_database():
    conn = sqlite3.connect("backend/"+DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cat_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE,
            created_at DATE DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    return conn

def insert_fact(conn, fact):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO cat_facts (fact) VALUES (?)', (fact,))
        conn.commit()
        print(f"Inserted fact: {fact}")
    except sqlite3.IntegrityError:
        print(f"Fact already exists: {fact}")