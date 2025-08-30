import string, secrets

def pass_strength_check(password):
    score = 0
    length = len(password)
    if length >= 8:
        score += 1 # Length check
    if any(c.islower() for c in password):
        score += 1 # Lowercase check
    if any(c.isupper() for c in password):
        score += 1 # Uppercase check
    if any(c.isdigit() for c in password):
        score += 1 # Digit check
    if any(c in string.punctuation for c in password):
        score += 1 # Special character check
    return score >= 4 # At least 4 out of 5 criteria met to be considered strong    
def generate_strong_password(length=12):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    
    while True:
        password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
        if pass_strength_check(password):
            return password # Ensure generated password is strong
# Example usage:
if __name__ == "__main__":
    test_password = input("Enter a password to check its strength: ")
    print(f"Password: {test_password}, Strong: {pass_strength_check(test_password)}")
    print(f"Generated strong password: {generate_strong_password(12)}") 
# File: pass_check.py
# Description: A simple module to check password strength and generate strong passwords. 
# Usage: Run the script and provide a password to check its strength or generate a strong password. 
# Note: This implementation is for educational purposes and may not cover all security aspects needed for production use. 
# Always use well-established libraries for production systems.
# Ensure to handle exceptions and edge cases in real-world applications. 
# Criteria for strong password: Minimum 8 characters, includes lowercase, uppercase, digits, and special characters.