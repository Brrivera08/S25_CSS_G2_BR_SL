from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Store temp users in memory (for demonstration)
temp_users = {}

def load_users(filename='users.txt'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    
    users = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':', 1)
                    users[username.strip()] = password.strip()
    except FileNotFoundError:
        print(f"[Error] User database file not found at: {file_path}")
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
            if username == 'HRManager':
                return redirect(url_for('hr_dashboard'))
            return redirect(url_for('success'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/success')
def success():
    if 'username' in session:
        return render_template('success.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/hr_dashboard', methods=['GET', 'POST'])
def hr_dashboard():
    if session.get('username') != 'HRManager':
        return redirect(url_for('login'))

    message = None
    if request.method == 'POST':
        new_user = request.form['new_user']
        new_pass = request.form['new_pass']
        duration = int(request.form['duration'])
        expiry = datetime.now() + timedelta(minutes=duration)
        temp_users[new_user] = {'password': new_pass, 'expires_at': expiry}
        message = f"Temporary user '{new_user}' created. Expires at {expiry.strftime('%Y-%m-%d %H:%M:%S')}."

    return render_template('hr_dashboard.html', temp_users=temp_users, message=message)

# Optional: A route to validate temp users (for demo)
@app.route('/validate_temp', methods=['POST'])
def validate_temp():
    data = request.form
    user = data['username']
    password = data['password']
    user_data = temp_users.get(user)
    now = datetime.now()

    if user_data and user_data['password'] == password and user_data['expires_at'] > now:
        return f"Temp login success for {user}"
    return "Temp login failed or expired"

if __name__ == '__main__':
    app.run(debug=True)
