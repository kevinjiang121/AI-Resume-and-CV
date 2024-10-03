import json

def read_experience(file_path='experience.json'):
    try:
        with open(file_path, 'r') as file:
            experience = json.load(file)
        return experience
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")