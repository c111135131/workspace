import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def init_database():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 創建 clients 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            ClientId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL
        );
    ''')

    # 創建 orders 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
            ClientId INTEGER NOT NULL,
            ItemName TEXT NOT NULL,
            Quantity INTEGER NOT NULL,
            Date TEXT NOT NULL,
            Status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (ClientId) REFERENCES clients (ClientId)
        );
    ''')

    conn.commit()
    conn.close()

def get_unprocessed_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT OrderId As 訂單編號, 
        ClientName As 客戶名稱, 
        GROUP_CONCAT(CONCAT(ItemName, '*', Quantity) SEPARATOR ', ') AS 商品明細
        FROM orders JOIN clients ON orders.ClientId = clients.ClientId 
        WHERE Status = 'pending' 
        ORDER BY Date;
    ''')
    orders = [
        {"OrderId": row[0], "ClientId": row[1], "ItemName": row[2], "Quantity": row[3]} 
        for row in cursor.fetchall()
    ]
    conn.close()
    return orders

# 獲取前一個月的 "YYYY-MM" 格式
def get_previous_month():
    today = datetime.today()
    first = today.replace(day=1)
    previous_month = first - timedelta(days=1)
    return previous_month.strftime("%Y-%m")

# 獲取前一個月的銷售報告
def get_monthly_sales_report():
    previous_month = get_previous_month()
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(Date), SUM(Quantity)
        FROM orders
        WHERE strftime('%Y-%m', Date) = ?
        GROUP BY DATE(Date)
        ORDER BY DATE(Date)
    """, (previous_month,))
    report = cursor.fetchall()
    conn.close()
    
    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in report]
    quantities = [row[1] for row in report]
    
    return dates, quantities

def get_completedOrder_client(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ClientId
        FROM orders
        WHERE id = ?
    """, (order_id,))
    client_id = cursor.fetchone()
    conn.close()
    return client_id[0] if client_id else None

def mark_order_as_completed(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE orders
        SET status = 'completed'
        WHERE id = ?
    """, (order_id,))
    conn.commit()
    conn.close()



