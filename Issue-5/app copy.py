from flask import Flask, render_template, request, redirect, url_for, session
import os, random, datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

temp_users = {}

def load_users(filename='users.txt'):
    path = os.path.join(os.path.dirname(__file__), filename)
    users = {}
    try:
        with open(path, 'r') as file:
            for line in file:
                if ':' in line:
                    username, password = line.strip().split(':', 1)
                    users[username.strip()] = password.strip()
    except FileNotFoundError:
        print("[Error] users.txt not found.")
    return users

def load_hr_status(filename='hr_status.txt'):
    path = os.path.join(os.path.dirname(__file__), filename)
    status = {}
    try:
        with open(path, 'r') as file:
            for line in file:
                if ':' in line:
                    username, state = line.strip().split(':', 1)
                    status[username.strip()] = state.strip().lower()
    except FileNotFoundError:
        print("[Error] hr_status.txt not found.")
    return status

def log_event(message, filename='logs.txt'):
    path = os.path.join(os.path.dirname(__file__), filename)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as file:
        file.write(f"[{timestamp}] {message}\n")

def revoke_access(username):
    # Simulate revocation of roles, sessions, etc.
    session.clear()
    log_event(f"Access revoked for offboarded user '{username}' (session terminated, roles cleared)")

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
            code = '123456' 
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

    hr_status = load_hr_status()
    username = session['username']
    if username in hr_status and hr_status[username] == "offboarded":
        revoke_access(username)
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
    if 'username' not in session:
        return redirect(url_for('login'))

    hr_status = load_hr_status()
    username = session['username']
    if username in hr_status and hr_status[username] == "offboarded":
        revoke_access(username)
        return redirect(url_for('login'))

    return render_template('success.html', username=username)

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
