import sqlite3

DB_PATH = "test_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_test_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_product(id, title, price, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)",
        (id, title, price, category)
    )
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE id=?", 
        (product_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result

def get_products_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE category=?",
        (category,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def clear_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    conn.commit()
    conn.close()