print("Spam Email Detection Project")

email = input("Enter email message: ")

spam_words = ["win", "free", "prize", "urgent", "offer"]

email = email.lower()

if any(word in email for word in spam_words):
    print("Prediction: Spam Email")
else:
    print("Prediction: Ham Email")