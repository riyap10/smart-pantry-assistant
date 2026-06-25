import sqlite3

def connect_db():
    conn = sqlite3.connect("pantry.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL,
            quantity INTEGER,
            expiration_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_ingredient(name, quantity, expiration_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pantry 
        (ingredient, quantity, expiration_date) 
        VALUES (?, ?, ?)
        """,
        (name, quantity, expiration_date)
    )
    conn.commit()
    conn.close() 

def view_pantry():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pantry")
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_recipe_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            is INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_text TEXT NOT NULL,
            saved_on TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_recipe(recipe_text):
    from datetime import date
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (recipe_text, saved_on) VALUES (?, ?)",
        (recipe_text, str(date.today()))
    )
    conn.commit()
    conn.close()

def view_recipes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    rows = cursor.fetchall()
    conn.close()
    return rows