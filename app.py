
from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector, os

app = Flask(__name__)
app.secret_key = 'supersecret'

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "user"),
        password=os.getenv("MYSQL_PASSWORD", "pass"),
        database=os.getenv("MYSQL_DATABASE", "ecommerce")
    )

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("index.html", products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/')
    return render_template("login.html")

@app.route('/order/<int:product_id>')
def order(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, product_id, status) VALUES (%s, %s, 'ordered')",
                   (session['user_id'], product_id))
    conn.commit()
    return redirect('/orders')

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, p.name, o.status FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.user_id = %s
    """, (session['user_id'],))
    data = cursor.fetchall()
    return render_template("orders.html", orders=data)

@app.route('/cancel/<int:order_id>')
def cancel(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status='cancelled' WHERE id=%s", (order_id,))
    conn.commit()
    return redirect('/orders')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
