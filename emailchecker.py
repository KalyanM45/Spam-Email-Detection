def check_email(message):
    spam_words = ["win", "prize", "free", "urgent", "lottery"]

    message = message.lower()

    for word in spam_words:
        if word in message:
            return "Spam Email"

    return "Not Spam"


email = input("Enter an email message: ")
result = check_email(email)

print("Result:", result)