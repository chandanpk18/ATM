import random
import mysql.connector
from mysql.connector import Error

# Constants
MAX_ATTEMPTS = 3
PIN_LENGTH = 4
INITIAL_BALANCE = 1000

def connect_db():
    """Connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',  # Replace with your MySQL username
            password='your_password',  # Replace with your MySQL password
            database='atm'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table():
    """Create the users table in the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            card_number INT PRIMARY KEY,
                            pin INT,
                            name VARCHAR(255),
                            phone_number VARCHAR(10),
                            balance DECIMAL(10, 2)
                        )''')
        conn.commit()
        cursor.close()
        conn.close()

def register():
    """Register a new user and generate a debit card and PIN."""
    name = input("Enter your name: ").strip()
    if not name.isalpha():
        print("Invalid name. Please enter a valid name.")
        return register()

    phno = input("Enter your mobile number: ").strip()
    if not phno.isdigit() or len(phno) != 10:
        print("Invalid phone number. Please enter a 10-digit number.")
        return register()

    debitno = random.randint(1000, 9999)
    print("Your generated debit card number is:", debitno)

    try:
        pin = int(input("Choose your ATM PIN: ").strip())
        if len(str(pin)) != PIN_LENGTH:
            print(f"Invalid PIN. Please choose a {PIN_LENGTH}-digit PIN.")
            return register()
    except ValueError:
        print(f"Invalid input. Please enter a {PIN_LENGTH}-digit number.")
        return register()

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (card_number, pin, name, phone_number, balance) 
                          VALUES (%s, %s, %s, %s, %s)''', (debitno, pin, name, phno, INITIAL_BALANCE))
        conn.commit()
        cursor.close()
        conn.close()

    print(f"Registration successful. Please remember your card number: {debitno} and PIN: {pin}")
    main_menu()

def atm():
    """Simulate ATM access and validate the user."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            card = int(input("Enter your card number: ").strip())
            atm_pin = int(input("Enter your PIN: ").strip())
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            attempts += 1
            print(f"Attempts left: {MAX_ATTEMPTS - attempts}")
            continue

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT pin FROM users WHERE card_number = %s''', (card,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and user[0] == atm_pin:
                function(card)
                return
            else:
                attempts += 1
                print(f"Invalid card number or PIN. Attempts left: {MAX_ATTEMPTS - attempts}")

    print("Account locked due to too many failed attempts.")

def function(card):
    """Provide ATM services such as cash withdrawal, balance check, and cash deposit."""
    while True:
        print("\nChoose an option:")
        print("1. Cash Withdrawal")
        print("2. Balance Check")
        print("3. Cash Deposit")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            try:
                amount = int(input("Enter amount to withdraw: ").strip())
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                continue

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT balance FROM users WHERE card_number = %s''', (card,))
                balance = cursor.fetchone()[0]

                if amount <= balance:
                    new_balance = balance - amount
                    cursor.execute('''UPDATE users SET balance = %s WHERE card_number = %s''', (new_balance, card))
                    conn.commit()
                    print(f"{amount} withdrawn successfully. Remaining balance: {new_balance}")
                else:
                    print("Insufficient balance.")

                cursor.close()
                conn.close()

        elif choice == '2':
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT balance FROM users WHERE card_number = %s''', (card,))
                balance = cursor.fetchone()[0]
                print(f"Your balance is: {balance}")
                cursor.close()
                conn.close()

        elif choice == '3':
            try:
                amount = int(input("Enter amount to deposit: ").strip())
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                continue

            if amount > 0:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute('''SELECT balance FROM users WHERE card_number = %s''', (card,))
                    balance = cursor.fetchone()[0]
                    new_balance = balance + amount
                    cursor.execute('''UPDATE users SET balance = %s WHERE card_number = %s''', (new_balance, card))
                    conn.commit()
                    print(f"{amount} deposited successfully. New balance: {new_balance}")
                    cursor.close()
                    conn.close()
            else:
                print("Invalid deposit amount. Please enter a positive number.")

        elif choice == '4':
            print("Thank you for using the ATM service.")
            break

        else:
            print("Invalid choice. Please try again.")

def main_menu():
    """Display the main menu for the ATM service."""
    while True:
        print("\nMain Menu:")
        print("1. Register for ATM service")
        print("2. ATM services")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            atm()
        elif choice == '3':
            print("Thank you for using the ATM service.")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

# Initialize the database and table
create_table()

# Start the program
main_menu()
