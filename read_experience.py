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

if __name__ == "__main__":
    experience = read_experience('experience.json')
    work_experience = experience['experience'][0]
    education = experience['education'][0]
    project = experience['projects'][0]
    skill = experience['skill'][0]
    print(skill)