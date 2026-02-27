import secrets
import string
import sys

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    """
    Generates a secure random password based on the given criteria.
    """
    if length < 4:
        print("Error: Password length should be at least 4 to include all character types.")
        return None

    chars = ""
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if not chars:
        print("Error: At least one character type must be selected.")
        return None

    # Ensure the password has at least one character of each selected type
    password = []
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_symbols:
        password.append(secrets.choice(string.punctuation))

    # Fill the rest of the password length
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(secrets.choice(chars))

    # Shuffle the characters to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)

def main():
    print("--- Secure Password Generator ---")
    try:
        length = int(input("Enter password length (default 16): ") or 16)
        
        include_upper = input("Include uppercase letters? (Y/n): ").lower() != 'n'
        include_lower = input("Include lowercase letters? (Y/n): ").lower() != 'n'
        include_digit = input("Include digits? (Y/n): ").lower() != 'n'
        include_symbol = input("Include symbols? (Y/n): ").lower() != 'n'

        password = generate_password(
            length=length,
            use_uppercase=include_upper,
            use_lowercase=include_lower,
            use_digits=include_digit,
            use_symbols=include_symbol
        )

        if password:
            print(f"\nYour Generated Password: {password}")
            print("-" * 30)
            
    except ValueError:
        print("Invalid input. Please enter a valid number for length.")

if __name__ == "__main__":
    main()
