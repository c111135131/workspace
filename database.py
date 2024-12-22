import sqlite3

# 資料庫初始化
def init_database():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            item_name TEXT,
            quantity INTEGER,
            status TEXT DEFAULT '未處理'
        )
    ''')
    conn.commit()
    conn.close()

# 獲取未處理訂單
def get_unprocessed_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, item_name, quantity FROM orders WHERE status = '未處理'")
    orders = [dict(zip(["id", "user_id", "item_name", "quantity"], row)) for row in cursor.fetchall()]
    conn.close()
    return orders

# 獲取銷售報表
def get_sales_report():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, SUM(quantity) FROM orders GROUP BY item_name")
    report = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return report
