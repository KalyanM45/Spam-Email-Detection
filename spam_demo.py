def detect_spam(message):
    spam_words = ["win", "prize", "free", "urgent", "claim"]

    for word in spam_words:
        if word in message.lower():
            return "Spam Email"

    return "Not Spam"


email = input("Enter an email message: ")
print(detect_spam(email))