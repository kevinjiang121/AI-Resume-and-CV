# generate_background.py

import tkinter as tk

def load_background_page(root, on_back):
    """
    Displays the background information page with options to create personal profile or experience detail.

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
        command=on_create_personal_profile,  # Placeholder function
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=25
    )
    button_create_personal_profile.pack(pady=5)

    button_create_experience_detail = tk.Button(
        buttons_frame,
        text="Create Experience Detail",
        command=on_create_experience_detail,  # Placeholder function
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=25
    )
    button_create_experience_detail.pack(pady=5)

    button_back_main = tk.Button(
        buttons_frame,
        text="Back",
        command=on_back,  # Call the on_back function
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=25
    )
    button_back_main.pack(pady=5)

def on_create_personal_profile():
    # Placeholder for future functionality
    pass

def on_create_experience_detail():
    # Placeholder for future functionality
    pass
