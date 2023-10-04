import random

# Sample user data structure (you can use a list of dictionaries)
users = []

def generate_unique_id():
    return random.randint(1000000000, 9999999999)

def generate_unique_username(name):
    return f"{name}{random.randint(1, 1000)}"



def create_account():
    name = input("Enter User Name: ")
    pin_code = input("Enter PIN Code: ")
    deposit_amount = float(input("Enter Initial Deposit Amount: Rs"))

    if deposit_amount <= 50:
        print("Deposit amount must be greater than Rs50.")
        return
    
    user = {
        "id": generate_unique_id(),
        "name": name,
        "username": generate_unique_username(name),
        "status": "ACTIVE",
        "currency": "PKR",
        "balance": deposit_amount,
        "pin_code": pin_code,
        "statement": [{"type": "DEPOSIT", "amount": deposit_amount}],
    }


    users.append(user)
    print("Account created successfully!")
    print(f"User Name: {user['name']}")
    print(f"Username: {user['username']}")
    print(f"Status: {user['status']}")
    print(f"Balance: Rs{user['balance']:.2f} {user['currency']}")
    print("Initial Deposit Transaction:")
    print(user['statement'][0])



def Checkin():
    username = input("Enter Username: ")
    user = find_user_by_username(username)

    if user is None:
        print("User not found.")
        return
    
    pin_attempts = 0
    while pin_attempts < 3:
        pin_code = input("Enter PIN Code: ")
        if pin_code == user["pin_code"]:
            print("Login successful!")
            sub_menu(user)
            return
        else:
            pin_attempts += 1
            print(f"Incorrect PIN. Attempts left: {3 - pin_attempts}")

    print("Too many incorrect PIN attempts. Account blocked.")
    user["status"] = "BLOCKED"
    save_users_data()


def sub_menu(user):
    while True:
        print("\nSUB MENU:")
        print("1. Account Detail")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Update PIN")
        print("5. Check Statement")
        print("6. Logout")
        choice = input("Enter Your Choice: ")


        if choice == "1":
            display_account_details(user)
        elif choice == "2":
            deposit_amount = float(input("Enter Deposit Amount: Rs"))
            deposit(user, deposit_amount)
        elif choice == "3":
            withdrawal_amount = float(input("Enter Withdrawal Amount: Rs"))
            withdraw(user, withdrawal_amount)
        elif choice == "4":
            update_pin(user)
        elif choice == "5":
            check_statement(user)
        elif choice == "6":
            print("Logged out successfully.")
            return
        else:
            print("Invalid choice. Please try again.")



def display_account_details(user):
    print("Account Details:")
    print(f"Name: {user['name']}")
    print(f"Username: {user['username']}")
    print(f"Status: {user['status']}")
    print(f"Balance: Rs{user['balance']:.2f} {user['currency']}")                



def deposit(user, amount):
    if amount <= 0:
        print("Deposit amount must be greater than zero.")
        return
    

    user["balance"] += amount
    user["statement"].append({"type": "DEPOSIT", "amount": amount})
    print(f"Deposit of Rs{amount:.2f} successful.")
    print(f"New Balance: Rs{user['balance']:.2f} {user['currency']}")
    save_users_data()
    
    
def withdraw(user, amount):
    if user["status"] == "BLOCKED":
        print("Account is blocked. Cannot withdraw.")
        return

    if amount <= 0:
        print("Withdrawal amount must be greater than zero.")
        return

    withdrawal_fee = amount * 0.01
    total_withdrawal = amount + withdrawal_fee

    if total_withdrawal > user["balance"]:
        print("Insufficient funds for withdrawal.")
        return

    user["balance"] -= total_withdrawal
    user["statement"].append({"type": "WITHDRAWAL", "amount": total_withdrawal})
    print(f"Withdrawal of Rs{amount:.2f} successful.")
    print(f"Withdrawal Fee: Rs{withdrawal_fee:.2f}")
    print(f"New Balance: Rs{user['balance']:.2f} {user['currency']}")
    save_users_data()
  

def update_pin(user):
    current_pin = input("Enter Current PIN: ")
    if current_pin == user["pin_code"]:
        new_pin = input("Enter New 4-digit PIN: ")
        if len(new_pin) == 4 and new_pin.isdigit():
            user["pin_code"] = new_pin
            print("PIN updated successfully.")
            save_users_data()
        else:
            print("Invalid PIN format. PIN must be 4 digits.")
    else:
        print("Incorrect current PIN. PIN update failed.")


def check_statement(user):
    with open(f"{user['username']}_statement.txt", "w") as file:
        for transaction in user["statement"]:
            file.write(f"{transaction['type']}: Rs{transaction['amount']:.2f}\n")


def find_user_by_username(username):
    for user in users:
        if user["username"] == username:
            return user
    return None


def save_users_data():
    # Implementing the code to save user data to a file (users.txt) here
    # You will need to save the users list with their attributes to a file
    with open("users.txt", "w") as file:
        for user in users:
            file.write(f"User ID: {user['id']}\n")
            file.write(f"Name: {user['name']}\n")
            file.write(f"Username: {user['username']}\n")
            file.write(f"Status: {user['status']}\n")
            file.write(f"Currency: {user['currency']}\n")
            file.write(f"Balance: {user['balance']}\n")
            file.write(f"PIN Code: {user['pin_code']}\n")
            file.write("Statement:\n")
            for statement in user['statement']:
                file.write(f"    {statement['type']}: {statement['amount']}\n")
            file.write("\n")

    


def logout():
    print("Exiting to Main Menu.")
                    
# Main menu
while True:
    print("MAIN MENU:")
    print("1. Create Account\n")
    print("""2. Checkin
    SUB MENU:
    1. Account Detail
    2. Deposit
    3. Withdraw
    4. Update pin
    5. Check Statement
    6. Logout\n""")
    print("3. Exit")

    
    choice = int(input("Enter Your Choice: "))

    if choice == 1:
        create_account()
    elif choice == 2:
        # Implement the check-in functionality here
        Checkin()
        choice = int(input("Enter Your Choice: "))
        if choice == 1:
            display_account_details()
        elif choice == 2:
            deposit()
        elif choice == 3:
            withdraw()
        elif choice == 4:
            update_pin()
        elif choice == 5:
            check_statement()
        elif choice == 6:
            logout()
        else:
            print("Invalid choice. Please try again.")    
        #print("Check-in functionality will be implemented here.")
    elif choice == 3:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
