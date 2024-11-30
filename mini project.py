from cryptography.fernet import Fernet
import os

# File to store passwords
PASSWORD_FILE = "passwords.dat"
KEY_FILE = "key.key"

# Generate or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return key

# Initialize encryption key
key = load_key()
cipher = Fernet(key)

# Save password
def save_password(service, username, password):
    encrypted_data = cipher.encrypt(f"{service}|{username}|{password}".encode())
    with open(PASSWORD_FILE, 'ab') as file:
        file.write(encrypted_data + b"\n")
    print(f"Password for {service} saved successfully!")

# Retrieve password
def retrieve_password(service):
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords saved yet.")
        return
    with open(PASSWORD_FILE, 'rb') as file:
        for line in file:
            decrypted_data = cipher.decrypt(line.strip()).decode()
            saved_service, username, password = decrypted_data.split("|")
            if saved_service == service:
                print(f"Service: {service}\nUsername: {username}\nPassword: {password}")
                return
    print(f"No password found for {service}.")

# Menu
def menu():
    while True:
        print("\nPassword Manager")
        print("1. Save Password")
        print("2. Retrieve Password")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            service = input("Enter the service name: ").strip()
            username = input("Enter the username: ").strip()
            password = input("Enter the password: ").strip()
            save_password(service, username, password)
        elif choice == '2':
            service = input("Enter the service name: ").strip()
            retrieve_password(service)
        elif choice == '3':
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    menu()