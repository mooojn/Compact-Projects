import random
import string

def generate_password(length=12):
    if length < 4:
        return "Password length should be at least 4 characters."

    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=length))
    return password

if __name__ == "__main__":
    print("🔐 Password Generator for New Users")
    try:
        length = int(input("Enter desired password length (default 12): ") or 12)
        password = generate_password(length)
        print("\nGenerated Password:", password)
    except ValueError:
        print("Please enter a valid number.")
