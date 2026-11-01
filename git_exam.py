email = input("Enter email message: ")

spam_words = ["win", "free", "prize", "offer", "urgent"]

email = email.lower()

count = 0

for word in spam_words:
    if word in email:
        count = count + 1

if count > 0:
    print("Spam Email")
else:
    print("Ham Email")
