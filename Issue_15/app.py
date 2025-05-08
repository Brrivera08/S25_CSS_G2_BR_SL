from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from collections import defaultdict
import os
from flask import flash

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

def write_password_change_log(username, details=""):
    path = os.path.join(os.path.dirname(__file__), 'password_change_log.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as file:
        file.write(f"[{timestamp}] [PASSWORD_RESET] user: {username} - {details}\n")

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
        return redirect(url_for('hr_home'))

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
        email = request.form.get('email')
        if not email:
            return "Missing email", 400

        # Simulate sending verification code
        session['reset_email'] = email
        session['reset_code'] = '123456'  # Static for testing
        print(f"[DEBUG] Sent code 123456 to {email}")
        return redirect(url_for('verify_reset_code'))

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
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        email = session.get('reset_email')
        if not new_password:
            return "Missing password field", 400

        print(f"[Simulation] Password for {email} changed to: {new_password}")
        write_password_change_log(email, "Password was updated")
        session.pop('reset_email', None)
        return render_template('login.html', error="Your password has been updated.")

    return render_template('set_new_password.html')

def get_pending_requests():
    # This is just an example; you should replace this with actual logic
    return [request for request in pending_requests if request['status'] == 'pending']

@app.route('/hr_home')
def hr_home():
    if session.get('username') != 'HRManager':
        return redirect(url_for('login'))

    pending_requests = get_pending_requests() 

    return render_template('hr_home.html', pending_requests=pending_requests)


# Sample requests
pending_requests = [
    {'id': 1, 'employee': 'alice', 'type': 'Access Level Increase', 'details': 'Requesting level 3 access'},
    {'id': 2, 'employee': 'bob', 'type': 'Time Extension', 'details': 'Extend temporary access by 1 hour'},
    {'id': 3, 'employee': 'charlie', 'type': 'Reinstatement', 'details': 'Reinstate account after offboarding'}
]

@app.route('/hr_approvals', methods=['GET', 'POST'])
def hr_approvals():
    if session.get('username') != 'HRManager':
        return redirect(url_for('login'))

    global pending_requests

    if request.method == 'POST':
        action = request.form.get('action')
        req_id = int(request.form.get('request_id'))

        request_entry = next((r for r in pending_requests if r['id'] == req_id), None)
        if request_entry:
            if action == 'approve':
                flash(f"✅ Approved request {req_id} for {request_entry['employee']}")
                write_audit_log("HR_APPROVE", session['username'], f"Approved: {request_entry}")
            elif action == 'deny':
                flash(f"❌ Denied request {req_id} for {request_entry['employee']}")
                write_audit_log("HR_DENY", session['username'], f"Denied: {request_entry}")
            pending_requests = [r for r in pending_requests if r['id'] != req_id]

    return render_template('hr_approvals.html', requests=pending_requests)

if __name__ == '__main__':
    app.run(debug=True)