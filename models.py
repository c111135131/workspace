import sqlite3
from datetime import datetime

class Order:
    def __init__(self, user_id, desserts, total_price, status='pending'):
        self.user_id = user_id
        self.desserts = desserts
        self.total_price = total_price
        self.status = status
        self.created_at = datetime.now()

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    desserts TEXT,
                    total_price REAL,
                    status TEXT,
                    created_at DATETIME
                )
            ''')
            conn.commit()

    def add_order(self, order):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO orders 
                (user_id, desserts, total_price, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (order.user_id, str(order.desserts), order.total_price, order.status, order.created_at))
            conn.commit()
            return cursor.lastrowid