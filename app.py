from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure random value in production

def load_users():
    with open('users.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                return redirect('/dashboard')

        return 'Invalid username or password', 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
