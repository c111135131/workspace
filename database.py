import sqlite3
from datetime import datetime, timedelta

def init_database():
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()

        # 創建 clients 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                ClientId TEXT PRIMARY KEY,
                Name TEXT NOT NULL,
                Phone TEXT NOT NULL
            );
        ''')

        # 創建 orders 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                OrderId INTEGER PRIMARY KEY,
                ClientId INTEGER NOT NULL,
                ItemName TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                Date TEXT NOT NULL,
                Status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (ClientId) REFERENCES clients (ClientId)
            );
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_unprocessed_orders():
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT OrderId AS 訂單編號, 
            Name AS 客戶名稱, 
            Phone AS 客戶電話,
            GROUP_CONCAT(ItemName || '*' || Quantity) AS 商品明細
            FROM orders
            JOIN clients ON orders.ClientId = clients.ClientId 
            WHERE Status = 'pending' 
            GROUP BY OrderId
            ORDER BY Date;
        ''')

        # 構建訂單數據列表
        orders = [
            {
                "訂單編號": row[0], 
                "客戶名稱": row[1], 
                "客戶電話": row[2],  # 添加客戶電話
                "商品明細": row[3]  # 商品明細將是由 GROUP_CONCAT 聚合的字符串
            }
            for row in cursor.fetchall()
        ]
        return orders
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

# 獲取前一個月的 "YYYY-MM" 格式
def get_previous_month():
    today = datetime.today()
    first = today.replace(day=1)
    previous_month = first - timedelta(days=1)
    return previous_month.strftime("%Y-%m")

# 獲取前一個月的銷售報告
def get_monthly_sales_report():
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        previous_month = get_previous_month()
        cursor.execute("""
            SELECT Date, SUM(Quantity) 
            FROM orders 
            WHERE strftime('%Y-%m', Date) = ?
            GROUP BY Date
            ORDER BY Date
        """, (previous_month,))
        report = cursor.fetchall()
        
        dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in report]
        quantities = [row[1] for row in report]
        
        return dates, quantities
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return [], []
    finally:
        conn.close()

def get_completedOrder_client(order_id):
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ClientId
            FROM orders
            WHERE id = ?
        """, (order_id,))
        client_id = cursor.fetchone()
        return client_id[0] if client_id else None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def mark_order_as_completed(order_id):
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders
            SET status = 'completed'
            WHERE id = ?
        """, (order_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def check_clientId(clientId):
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT clientId
            FROM clients
            WHERE clientId = ?
        """, (clientId,))
        result = cursor.fetchone()  # 獲取單行結果
        return result is not None  # 如果存在結果，則返回 True，否則返回 False
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

# 將用戶資料存入資料庫
def save_user_to_database(ClientId, Name, Phone):
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (ClientId, Name, Phone)
            VALUES (?, ?, ?)
        ''', (ClientId, Name, Phone))  # 傳遞參數
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def save_order_to_db(OrderId, ClientId, orders):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # 當前日期時間
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入訂單資料
    for order in orders:
        cursor.execute('''
            INSERT INTO orders (OrderId, ClientId, ItemName, Quantity, Date, Status)
            VALUES (?, ?, ?, ?, ?)
        ''', (OrderId, ClientId, order['item'], order['quantity'], date, 'pending'))
    
    conn.commit()
    conn.close()
