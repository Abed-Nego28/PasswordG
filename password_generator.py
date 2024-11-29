import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_special_chars=True):
    """
    Generate a secure random password based on given criteria.

    :param length: Length of the password (default: 12)
    :param use_uppercase: Include uppercase letters (default: True)
    :param use_digits: Include digits (default: True)
    :param use_special_chars: Include special characters (default: True)
    :return: A randomly generated password.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Define character pools
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ''
    digits = string.digits if use_digits else ''
    special = string.punctuation if use_special_chars else ''

    all_chars = lower + upper + digits + special

    if not all_chars:
        raise ValueError("At least one character type must be selected.")

    # Ensure the password contains at least one of each selected character type
    password = []
    if use_uppercase:
        password.append(random.choice(upper))
    if use_digits:
        password.append(random.choice(digits))
    if use_special_chars:
        password.append(random.choice(special))
    password.append(random.choice(lower))

    # Fill the rest of the password length with random choices
    remaining_length = length - len(password)
    password += random.choices(all_chars, k=remaining_length)

    # Shuffle the password to ensure randomness
    random.shuffle(password)

    return ''.join(password)

def main():
    print("Welcome to the Password Generator!")

    try:
        length = int(input("Enter the desired password length (minimum 4): "))
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_special_chars = input("Include special characters? (y/n): ").lower() == 'y'

        password = generate_password(length, use_uppercase, use_digits, use_special_chars)
        print(f"Your generated password is: {password}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
