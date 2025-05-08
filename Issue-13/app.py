from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from collections import defaultdict
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

temp_users = {}

# Track failed login attempts
failed_logins = defaultdict(int)

def log_alert(message, filename='logs.txt'):
    path = os.path.join(os.path.dirname(__file__), filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_message = f"[{timestamp}] [ALERT] {message}"
    print(alert_message)
    with open(path, 'a') as file:
        file.write(alert_message + "\n")

def write_audit_log(event_type, username, details=""):
    path = os.path.join(os.path.dirname(__file__), 'audit_log.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as file:
        file.write(f"[{timestamp}] [{event_type}] user: {username} - {details}\n")

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
        hr_status = load_hr_status()

        # Deny access for offboarded users
        if username in hr_status and hr_status[username] == "offboarded":
            error = "Access denied: user is offboarded."
            log_alert(f"Blocked login attempt for OFFBOARDED user '{username}'")
            return render_template('login.html', error=error)

        if username in users and users[username] == password:
            failed_logins[username] = 0  # reset counter
            session['username'] = username
            write_audit_log("LOGIN", username, "Successful login")
            code = '123456'
            session['2fa_code'] = code
            print(f"[2FA] Code for {username}: {code}")
            return redirect(url_for('verify'))
        else:
            failed_logins[username] += 1
            error = "Invalid username or password"
            if failed_logins[username] >= 3:
                log_alert(f"Suspicious login pattern: 3+ failed attempts for user '{username}'")
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

    if username == 'HRManager':
        return redirect(url_for('hr_dashboard'))

    return render_template('success.html', username=username)

def alerts():
    if session.get('username') != 'admin':
        return redirect(url_for('login'))

    log_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
    alerts = []

    # Load alerts from logs.txt
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            for line in file:
                if '[ALERT]' in line:
                    parts = line.strip().split('] ', 2)
                    timestamp = parts[0].replace('[', '')
                    message = parts[-1].replace('[ALERT] ', '')
                    reviewed = '[REVIEWED]' in line
                    alerts.append({
                        'timestamp': timestamp,
                        'message': message.replace('[REVIEWED]', '').strip(),
                        'reviewed': reviewed
                    })

    # Handle POST to mark alert as reviewed (simulated in memory)
    if request.method == 'POST':
        index = int(request.form['reviewed'])
        alerts[index]['reviewed'] = True
        # Optionally: update file here (advanced version)

    return render_template('alerts.html', alerts=alerts)

@app.route('/hr_dashboard', methods=['GET', 'POST'])
def hr_dashboard():
    if session.get('username') != 'HRManager':
        return redirect(url_for('login'))

    global temp_users  # make sure you can update the temp_users dictionary
    message = None

    if request.method == 'POST':
        try:
            new_user = request.form['new_user'].strip()
            new_pass = request.form['new_pass'].strip()
            access_level = int(request.form['access_level'])
            duration = int(request.form['duration'])

            if not (1 <= access_level <= 5):
                raise ValueError("Invalid access level")

            expiry = datetime.now() + timedelta(minutes=duration)

            temp_users[new_user] = {
                'password': new_pass,
                'access_level': access_level,
                'expires_at': expiry.strftime('%Y-%m-%d %H:%M:%S')
            }

            write_audit_log("ROLE_ASSIGN", session['username'], f"Gave temporary access to '{new_user}' (level {access_level}, {duration} mins)")

            message = f"Temporary user '{new_user}' created with Access Level {access_level}, expires at {expiry.strftime('%Y-%m-%d %H:%M:%S')}."

        except (KeyError, ValueError) as e:
            message = f"Error processing request: {str(e)}"

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

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']

        # Example: assume username is stored in session
        username = session.get('username', 'unknown_user')

        # Log the change
        log_password_change(username)

        return redirect(url_for('login'))  # or success page
    return render_template('reset_password.html')


@app.route('/verify_reset_code', methods=['GET', 'POST'])
def verify_reset_code():
    error = None
    if request.method == 'POST':
        code = request.form.get('code')
        if code == session.get('reset_code'):
            session.pop('reset_code', None)
            return redirect(url_for('set_new_password'))
        else:
            error = "Incorrect verification code."
    return render_template('verify_reset_code.html', error=error)

@app.route('/set_new_password', methods=['GET', 'POST'])
def set_new_password():
    message = None
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        email = session.get('reset_email')
        # You would update the user's password in the real database here
        print(f"[Simulation] Password for {email} changed to: {new_password}")
        write_audit_log("PASSWORD_RESET", email, "Password was updated")
        session.pop('reset_email', None)
        message = "Your password has been updated. Please log in."
        return render_template('login.html', error=message)
    return render_template('set_new_password.html')

def log_password_change(username, filename='password_change_log.txt'):
    log_path = os.path.join(os.path.dirname(__file__), filename)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'a') as log_file:
        log_file.write(f"[{timestamp}] Password changed for user: {username}\n")

if __name__ == '__main__':
    app.run(debug=True)
