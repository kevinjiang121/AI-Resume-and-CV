# generate_background.py

import tkinter as tk
import os
import json
from tkinter import messagebox

def load_background_page(root, on_back):
    """
    Displays the background information page with options to create personal profile or experience history.

    :param root: The main Tkinter window.
    :param on_back: A callback function to return to the main page.
    """
    # Clear existing widgets from root window
    for widget in root.winfo_children():
        widget.pack_forget()

    label_background_info = tk.Label(root, text="Background Information Page", font=("Arial", 16))
    label_background_info.pack(pady=(20, 20))

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(0, 20))

    button_create_personal_profile = tk.Button(
        buttons_frame,
        text="Create Personal Profile",
        command=lambda: on_create_personal_profile(root, on_back, load_background_page),
        font=("Arial", 12),
        bg="blue",   # Blue button (non-navigation)
        fg="white",
        width=25
    )
    button_create_personal_profile.pack(pady=5)

    button_create_experience_history = tk.Button(
        buttons_frame,
        text="Create Experience History",
        command=lambda: on_create_experience_history(root, on_back, load_background_page),
        font=("Arial", 12),
        bg="blue",   # Blue button (non-navigation)
        fg="white",
        width=25
    )
    button_create_experience_history.pack(pady=5)

    button_back_main = tk.Button(
        buttons_frame,
        text="Back",
        command=on_back,  # Call the on_back function
        font=("Arial", 12),
        bg="red",    # Red button (navigation)
        fg="white",
        width=25
    )
    button_back_main.pack(pady=5)

def on_create_personal_profile(root, on_back, load_background_page):
    """
    Displays the personal profile creation page with four text boxes and three buttons.

    :param root: The main Tkinter window.
    :param on_back: A callback function to return to the main page.
    :param load_background_page: Function to load the background page.
    """
    # Clear existing widgets from root window
    for widget in root.winfo_children():
        widget.pack_forget()

    label_title = tk.Label(root, text="Create Personal Profile", font=("Arial", 16))
    label_title.pack(pady=(20, 10))

    # Create a frame for the entries
    entries_frame = tk.Frame(root)
    entries_frame.pack(pady=(0, 20))

    # Name
    label_name = tk.Label(entries_frame, text="Name:", font=("Arial", 12))
    label_name.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_name = tk.Entry(entries_frame, width=50, font=("Arial", 12))
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    # Email
    label_email = tk.Label(entries_frame, text="Email:", font=("Arial", 12))
    label_email.grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_email = tk.Entry(entries_frame, width=50, font=("Arial", 12))
    entry_email.grid(row=1, column=1, padx=5, pady=5)

    # Phone Number
    label_phone = tk.Label(entries_frame, text="Phone Number:", font=("Arial", 12))
    label_phone.grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_phone = tk.Entry(entries_frame, width=50, font=("Arial", 12))
    entry_phone.grid(row=2, column=1, padx=5, pady=5)

    # Github
    label_github = tk.Label(entries_frame, text="Github:", font=("Arial", 12))
    label_github.grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_github = tk.Entry(entries_frame, width=50, font=("Arial", 12))
    entry_github.grid(row=3, column=1, padx=5, pady=5)

    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(10, 20))

    # Back to Main Page
    button_back_main = tk.Button(
        buttons_frame,
        text="Back to Main Page",
        command=on_back,
        font=("Arial", 12),
        bg="red",    # Red button (navigation)
        fg="white",
        width=18
    )
    button_back_main.pack(side=tk.LEFT, padx=5)

    # Back to Create Background Page
    button_back_background = tk.Button(
        buttons_frame,
        text="Back to Background Page",
        command=lambda: load_background_page(root, on_back),
        font=("Arial", 12),
        bg="red",    # Red button (navigation)
        fg="white",
        width=22
    )
    button_back_background.pack(side=tk.LEFT, padx=5)

    # Submit Profile
    button_submit_profile = tk.Button(
        buttons_frame,
        text="Submit Profile",
        command=lambda: submit_profile(entry_name, entry_email, entry_phone, entry_github),
        font=("Arial", 12),
        bg="blue",   # Blue button (non-navigation)
        fg="white",
        width=18
    )
    button_submit_profile.pack(side=tk.LEFT, padx=5)

def submit_profile(entry_name, entry_email, entry_phone, entry_github):
    """
    Retrieves the user's input from the text boxes and saves it as a JSON file.

    :param entry_name: Entry widget for the Name.
    :param entry_email: Entry widget for the Email.
    :param entry_phone: Entry widget for the Phone Number.
    :param entry_github: Entry widget for the Github.
    """
    # Retrieve the input values
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    phone = entry_phone.get().strip()
    github = entry_github.get().strip()

    # Create a dictionary with the input values
    profile_data = {
        "Name": name,
        "Email": email,
        "Phone Number": phone,
        "Github": github
    }

    # Directory where the JSON file will be saved
    directory = "Background and Experience"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # File path for the JSON file
    file_path = os.path.join(directory, "personal_profile.json")

    try:
        # Save the dictionary as a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(profile_data, json_file, indent=4)

        # Show a success message
        messagebox.showinfo("Success", f"Personal profile saved successfully in '{file_path}'.\n\nlatexconfig.py will now retrieve these values.")
    except Exception as e:
        # Show an error message if something goes wrong
        messagebox.showerror("Error", f"An error occurred while saving the profile:\n{e}")

def on_create_experience_history(root, on_back, load_background_page):
    """
    Displays the experience history creation page with section titles and navigation buttons.

    :param root: The main Tkinter window.
    :param on_back: A callback function to return to the main page.
    :param load_background_page: Function to load the background page.
    """
    # Clear existing widgets from root window
    for widget in root.winfo_children():
        widget.pack_forget()

    label_title = tk.Label(root, text="Create Experience History", font=("Arial", 16))
    label_title.pack(pady=(20, 10))

    # Create a frame to hold all sections
    sections_frame = tk.Frame(root)
    sections_frame.pack(pady=(0, 20), fill=tk.BOTH, expand=True)

    # Define the sections
    sections = ["Work Experience", "Education", "Projects", "Skills"]

    for i, section_name in enumerate(sections):
        # Section label
        label = tk.Label(sections_frame, text=section_name, font=("Arial", 12))
        label.pack(anchor='w', padx=10, pady=(10 if i == 0 else 0, 5))

        # Separator line except after the last section
        if i < len(sections) - 1:
            separator = tk.Frame(sections_frame, height=1, bd=1, relief=tk.SUNKEN, bg='grey')
            separator.pack(fill=tk.X, padx=10, pady=10)

    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(10, 20))

    # Back to Main Page
    button_back_main = tk.Button(
        buttons_frame,
        text="Back to Main Page",
        command=on_back,
        font=("Arial", 12),
        bg="red",    # Red button (navigation)
        fg="white",
        width=18
    )
    button_back_main.pack(side=tk.LEFT, padx=5)

    # Back to Create Background Page
    button_back_background = tk.Button(
        buttons_frame,
        text="Back to Background Page",
        command=lambda: load_background_page(root, on_back),
        font=("Arial", 12),
        bg="red",    # Red button (navigation)
        fg="white",
        width=22
    )
    button_back_background.pack(side=tk.LEFT, padx=5)

    # Submit Experience
    button_submit_experience = tk.Button(
        buttons_frame,
        text="Submit Experience",
        command=lambda: submit_experience(),
        font=("Arial", 12),
        bg="blue",   # Blue button (non-navigation)
        fg="white",
        width=18
    )
    button_submit_experience.pack(side=tk.LEFT, padx=5)

def submit_experience():
    # For now, this function does nothing
    pass
