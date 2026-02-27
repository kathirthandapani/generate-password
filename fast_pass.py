import secrets
import string
import time

def generate_password(length=16):
    """Ultra-fast secure password generation."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))

def main():
    print("--- INSTANT PASSWORD GENERATOR ---")
    try:
        # Measure time
        start_time = time.time()
        
        # Default to 16 for speed, no prompts
        password = generate_password(16)
        
        end_time = time.time()
        
        print(f"\nPassword: {password}")
        print(f"Generated in: {(end_time - start_time) * 1000:.4f}ms")
        print("-" * 30)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
