import sqlite3
import matplotlib.pyplot as plt

def get_unprocessed_orders():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE status='待確認'")
    orders = c.fetchall()
    conn.close()
    return orders

def get_orders_by_date(date):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE DATE(created_at) = ?", (date,))
    orders = c.fetchall()
    conn.close()
    return orders

def generate_sales_report(year):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("""
        SELECT strftime('%m', created_at) AS month, SUM(quantity) 
        FROM orders WHERE strftime('%Y', created_at) = ? GROUP BY month
    """, (year,))
    data = c.fetchall()
    conn.close()

    months = [int(row[0]) for row in data]
    sales = [row[1] for row in data]

    plt.bar(months, sales)
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.title(f'Sales Report for {year}')
    plt.savefig('static/sales_report.png')
    return 'static/sales_report.png'