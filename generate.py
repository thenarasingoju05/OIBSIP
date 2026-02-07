import random
import string
# INPUT VALIDATION FUNCTIONS
def get_password_length():
    while True:
        try:
            length = int(input("Enter password length (min 6): "))
            if length < 6:
                print("Password length must be at least 6.")
            else:
                return length
        except ValueError:
            print(" Please enter a valid number.")

def get_user_choice(prompt):
    while True:
        choice = input(prompt + " (y/n): ").lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Invalid input. Enter y or n.")
# PASSWORD GENERATOR
def generate_password(length, use_letters, use_numbers, use_symbols):
    characters = ""

    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        print("At least one character type must be selected.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password
# MAIN PROGRAM
def main():
    print(" Password Generator")

    length = get_password_length()

    use_letters = get_user_choice("Include letters?")
    use_numbers = get_user_choice("Include numbers?")
    use_symbols = get_user_choice("Include symbols?")

    password = generate_password(length, use_letters, use_numbers, use_symbols)

    if password:
        print("\nGenerated Password:")
        print(password)
main()
