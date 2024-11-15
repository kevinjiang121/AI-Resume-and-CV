# latexconfig.py

import json
import os

def name():
    return get_value("Name")

def email():
    return get_value("Email")

def phonenumber():
    return get_value("Phone Number")

def github():
    return get_value("Github")

def get_value(key):
    """
    Retrieves the value associated with the given key from the personal_profile.json file.
    """
    file_path = os.path.join("Background and Experience", "personal_profile.json")
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data.get(key, "")
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""
    
if __name__ == "__main__":
    print(name())