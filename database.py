import sqlite3

def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            item TEXT,
            quantity INTEGER,
            status TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_order(user_id, item, quantity, status):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, item, quantity, status) VALUES (?, ?, ?, ?)",
              (user_id, item, quantity, status))
    conn.commit()
    conn.close()