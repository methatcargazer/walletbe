import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "wallet.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(date, t_type, amount, category, description):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (date, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
        (date, t_type, amount, category, description)
    )
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date", conn)
    conn.close()
    return df

def monthly_report(year, month):
    conn = sqlite3.connect(DB_FILE)
    query = f"""
        SELECT type, SUM(amount) as total 
        FROM transactions 
        WHERE strftime('%Y', date) = '{year}' 
        AND strftime('%m', date) = '{month:02d}'
        GROUP BY type
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if df.empty:
        return None
    income = df[df['type'] == 'income']['total'].sum()
    expense = df[df['type'] == 'expense']['total'].sum()
    savings = income - expense
    return income, expense, savings
