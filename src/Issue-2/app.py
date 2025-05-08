from flask import Flask, render_template, request, redirect, url_for, session
import os, random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users(filename='users.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    users = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    username, password = line.strip().split(':', 1)
                    users[username.strip()] = password.strip()
    except FileNotFoundError:
        print(f"[Error] User file not found at {file_path}")
    return users

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            code = '123456' #example
            session['2fa_code'] = code
            print(f"[2FA] Code for {username}: {code}") 
            return redirect(url_for('verify'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    error = None
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        code = request.form['code']
        if code == session.get('2fa_code'):
            session.pop('2fa_code', None)
            return redirect(url_for('success'))
        else:
            error = "Invalid verification code"
    return render_template('verify.html', error=error)

@app.route('/success')
def success():
    if 'username' in session:
        return render_template('success.html', username=session['username'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
