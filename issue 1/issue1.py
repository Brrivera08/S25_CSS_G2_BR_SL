from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

DB = 'users.db'

# Database setup
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Create a test user (username: admin, password: password123)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       ('admin', generate_password_hash('password123')))
    except sqlite3.IntegrityError:
        pass  # User already exists
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
