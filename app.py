from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Create DB
def init_db():
    conn = sqlite3.connect("shop.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')

    # Insert sample products
    conn.execute("INSERT OR IGNORE INTO products VALUES (1,'Laptop',50000)")
    conn.execute("INSERT OR IGNORE INTO products VALUES (2,'Phone',20000)")
    conn.execute("INSERT OR IGNORE INTO products VALUES (3,'Headphones',2000)")
    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def index():
    conn = sqlite3.connect("shop.db")
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('index.html', products=products)

# ADD TO CART
@app.route('/add/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(id)
    session.modified = True
    return redirect('/')

# VIEW CART
@app.route('/cart')
def cart():
    if 'cart' not in session:
        return render_template('cart.html', items=[], total=0)

    conn = sqlite3.connect("shop.db")
    items = []
    total = 0

    for item_id in session['cart']:
        product = conn.execute("SELECT * FROM products WHERE id=?", (item_id,)).fetchone()
        items.append(product)
        total += product[2]

    conn.close()
    return render_template('cart.html', items=items, total=total)

# REMOVE ITEM
@app.route('/remove/<int:id>')
def remove_item(id):
    if 'cart' in session and id in session['cart']:
        session['cart'].remove(id)
        session.modified = True
    return redirect('/cart')

# CHECKOUT
@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)