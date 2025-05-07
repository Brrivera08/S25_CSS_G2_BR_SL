import getpass

# Load user data from a file
import os

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


# Authenticate user credentials
def authenticate(users, username, password):
    return users.get(username) == password

# Main login system
def main():
    print("=== Secure Login System ===")
    users = load_users()
    if not users:
        print("[Error] No users found. Please set up users.txt.")
        return

    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        if authenticate(users, username, password):
            print(f"\n[Success] Welcome, {username}!")
            # Proceed to system (placeholder)
            enter_system(username)
            return
        else:
            attempts -= 1
            print(f"[Error] Invalid credentials. Attempts left: {attempts}")

    print("\n[Access Denied] Too many failed attempts.")

# Placeholder for the system the user gains access to
def enter_system(username):
    print(f"Access granted to {username}. You're now inside the system.")
    # You can expand this function with real functionality

if __name__ == '__main__':
    main()

