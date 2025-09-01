"""
Simple Python file for testing obfuscation.
"""

def greet(name):
    """Greet a person by name."""
    greeting = f"Hello, {name}!"
    return greeting

def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    area = length * width
    return area

def main():
    """Main function."""
    user_name = "Alice"
    room_length = 10
    room_width = 12
    
    message = greet(user_name)
    room_area = calculate_area(room_length, room_width)
    
    print(message)
    print(f"Room area: {room_area} square units")

if __name__ == "__main__":
    main()
