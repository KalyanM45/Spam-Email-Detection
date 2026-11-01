
# Spam Email Detection Program

def check_spam(email):
    spam_words = ["win", "prize", "free", "offer",
                  "lottery", "urgent"]

    email = email.lower()

    for word in spam_words:
        if word in email:
            return "Spam Email"

    return "Ham (Not Spam)"


email = input("Enter your email message: ")

result = check_spam(email)

print("Email Classification:", result)
