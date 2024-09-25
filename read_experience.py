import json

def read_experience(file_path='experience.json'):

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    experience_data = read_experience('experience.json')
    if experience_data:
        print("Experience Data:")
        print("-----------------")
        print(json.dumps(experience_data, indent=4))
    else:
        print("No experience data found.")
