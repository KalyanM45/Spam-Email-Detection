# Program to check palindrome

string = input("Enter a string: ")

if string == string[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")