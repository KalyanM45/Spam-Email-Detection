

def check_email():
    email = input("Enter email: ")

    if "win" in email.lower() or "prize" in email.lower():
        print("Warning: Suspicious Email")
    else:
        print("Email entered successfully")

check_email()