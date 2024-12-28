import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

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
            Date TIME NOT NULL,
            Status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (ClientId) REFERENCES clients (ClientId)
        );
    ''')

    conn.commit()
    conn.close()


# 獲取未處理訂單
def get_unprocessed_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT OrderId, ClientId, ItemName, Quantity FROM orders WHERE Status = 'pending' ORDER BY Date")
    orders = [
        {"OrderId": row[0], "ClientId": row[1], "ItemName": row[2], "Quantity": row[3]} 
        for row in cursor.fetchall()
    ]
    conn.close()
    return orders

def get_monthly_sales_report():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    # 查詢每一天的銷售數量，按日期分組
    cursor.execute("""
        SELECT Date, SUM(Quantity) 
        FROM orders 
        WHERE strftime('%Y-%m', Date) = strftime('%Y-%m', 'now')  -- 只查詢當月數據
        GROUP BY Date
        ORDER BY Date
    """)
    report = cursor.fetchall()
    conn.close()
    
    # 組織數據以便繪製
    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in report]
    quantities = [row[1] for row in report]
    
    return dates, quantities

# 繪製銷售折線圖
def plot_sales_line_chart():
    dates, quantities = get_monthly_sales_report()
    
    # 畫圖
    plt.figure(figsize=(10, 6))
    plt.plot(dates, quantities, marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
    plt.title("Monthly Sales Report", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Sales Quantity", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # 顯示圖表
    plt.tight_layout()
    plt.savefig("image/monthly_sales_report.png")
