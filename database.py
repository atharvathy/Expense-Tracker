import sqlite3
import os

DB_NAME = "expenses.db"

def get_connection(db_path=DB_NAME):
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DB_NAME):
    """Initializes the database schema if tables do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('Expense', 'Income')),
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            payment_method TEXT DEFAULT 'Cash',
            note TEXT DEFAULT ''
        )
    ''')
    
    # Create budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            monthly_limit REAL NOT NULL
        )
    ''')
    
    # Seed default budget limits if empty
    cursor.execute("SELECT COUNT(*) as count FROM budgets")
    if cursor.fetchone()['count'] == 0:
        default_budgets = [
            ('Food & Dining', 500.0),
            ('Housing & Rent', 1200.0),
            ('Transportation', 250.0),
            ('Entertainment', 200.0),
            ('Utilities', 300.0),
            ('Shopping', 350.0),
            ('Health & Medical', 200.0),
            ('Miscellaneous', 150.0)
        ]
        cursor.executemany("INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)", default_budgets)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
