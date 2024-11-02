# gui.py

import tkinter as tk
from tkinter import messagebox
import json
import os
import renderer  # Ensure renderer.py is in the same directory or adjust the import path accordingly

def on_generate():
    # Handler for the Generate button.
    file_name = entry_filename.get().strip()
    if not file_name:
        messagebox.showwarning("Input Required", "Please enter a file name for the PDF.")
        return
    
    try:
        success = renderer.generate_pdf(file_name)
        if success:
            messagebox.showinfo("Success", f"PDF '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")
    except Exception as e:
        messagebox.showerror("Failure", f"PDF generation failed.\n\n{e}")

def load_background_page():
    """
    Clears the main GUI content and loads a new layout with two placeholder buttons.
    """
    # Hide main widgets
    for widget in root.winfo_children():
        widget.pack_forget()

    # Add two placeholder buttons and a back button to this layout
    button_personal_detail = tk.Button(
        root,
        text="Personal Detail",
        font=("Arial", 12),
        width=18,
        bg="blue",
        fg="white",
        command=load_personal_detail_page
    )
    button_personal_detail.pack(pady=(20, 10))

    button_create_background = tk.Button(
        root,
        text="Create Background",
        font=("Arial", 12),
        width=18,
        bg="blue",
        fg="white"
    )
    button_create_background.pack(pady=(10, 20))

    # Back Button to return to the main page
    button_back = tk.Button(
        root,
        text="Back",
        command=load_main_page,
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=18
    )
    button_back.pack(pady=(10, 10))

def create_personal_profile():
    """
    Creates a JSON file with personal details entered by the user.
    """
    # Get input values from textboxes
    profile_data = {
        "Name": entry_name.get().strip(),
        "Email": entry_email.get().strip(),
        "Phone Number": entry_phone.get().strip(),
        "GitHub": entry_github.get().strip()
    }

    # Check if all fields have been filled
    if not all(profile_data.values()):
        messagebox.showwarning("Input Required", "Please fill in all fields before creating the profile.")
        return

    # Define file path
    file_path = os.path.join("Background and Experience", "personal_profile.json")

    try:
        # Write to JSON file
        with open(file_path, 'w') as json_file:
            json.dump(profile_data, json_file, indent=4)
        messagebox.showinfo("Success", f"Personal profile has been saved to '{file_path}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create personal profile.\n\n{e}")

def load_personal_detail_page():
    """
    Clears the current layout and loads a new page with five textboxes for personal details
    and three buttons (Back to Previous, Back to Main, Create Personal Profile).
    """
    global entry_name, entry_email, entry_phone, entry_github

    # Clear current widgets
    for widget in root.winfo_children():
        widget.pack_forget()

    # Labels and Entry Widgets for Personal Details
    label_name = tk.Label(root, text="Name:", font=("Arial", 12))
    label_name.pack(pady=(10, 5))
    entry_name = tk.Entry(root, width=50, font=("Arial", 12))
    entry_name.pack(pady=(0, 10))

    label_email = tk.Label(root, text="Email:", font=("Arial", 12))
    label_email.pack(pady=(10, 5))
    entry_email = tk.Entry(root, width=50, font=("Arial", 12))
    entry_email.pack(pady=(0, 10))

    label_phone = tk.Label(root, text="Phone Number:", font=("Arial", 12))
    label_phone.pack(pady=(10, 5))
    entry_phone = tk.Entry(root, width=50, font=("Arial", 12))
    entry_phone.pack(pady=(0, 10))

    label_github = tk.Label(root, text="GitHub:", font=("Arial", 12))
    label_github.pack(pady=(10, 5))
    entry_github = tk.Entry(root, width=50, font=("Arial", 12))
    entry_github.pack(pady=(0, 10))

    # Buttons Frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(20, 10))

    # Back to Previous Page Button
    button_back_previous = tk.Button(
        buttons_frame,
        text="Back to Previous",
        command=load_background_page,
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=18
    )
    button_back_previous.pack(side=tk.LEFT, padx=5)

    # Back to Main Page Button
    button_back_main = tk.Button(
        buttons_frame,
        text="Back to Main",
        command=load_main_page,
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=18
    )
    button_back_main.pack(side=tk.LEFT, padx=5)

    # Create Personal Profile Button
    button_create_profile = tk.Button(
        buttons_frame,
        text="Create Personal Profile",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=18,
        command=create_personal_profile
    )
    button_create_profile.pack(side=tk.LEFT, padx=5)

def load_main_page():
    """
    Restores the main page layout for file name entry and job description.
    """
    # Clear background page widgets
    for widget in root.winfo_children():
        widget.pack_forget()

    # Repack main widgets
    label_filename.pack(pady=(20, 5))
    entry_filename.pack(pady=(0, 10))
    label_job_description.pack(pady=(0, 5))
    text_job_description.pack(pady=(0, 20))
    buttons_frame.pack(pady=(0, 20))

def on_test():
    # Handler for the Test button.
    prompt = text_job_description.get("1.0", "end-1c").strip()
    if not prompt or prompt == "Job Description":
        messagebox.showwarning("Input Required", "Please enter a job description before testing.")
        return
    
    try:
        renderer.call_openai_assistant(prompt)
        messagebox.showinfo("Success", "OpenAI Assistant has processed your job description.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while calling OpenAI Assistant:\n{e}")

# Function to handle placeholder text in the Job Description Text widget
def on_focus_in(event):
    if text_job_description.get("1.0", "end-1c") == "Job Description":
        text_job_description.delete("1.0", "end")
        text_job_description.config(fg="black")

def on_focus_out(event):
    if text_job_description.get("1.0", "end-1c") == "":
        text_job_description.insert("1.0", "Job Description")
        text_job_description.config(fg="grey")

# Setting up the GUI
root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("700x600")
root.resizable(False, False)

# Main Page Widgets
label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
entry_filename = tk.Entry(root, width=60, font=("Arial", 12))

label_job_description = tk.Label(root, text="Job Description:", font=("Arial", 12))
text_job_description = tk.Text(root, width=60, height=15, font=("Arial", 12), fg="grey")
text_job_description.insert("1.0", "Job Description")
text_job_description.bind("<FocusIn>", on_focus_in)
text_job_description.bind("<FocusOut>", on_focus_out)

buttons_frame = tk.Frame(root)

button_generate = tk.Button(
    buttons_frame,
    text="Generate PDF",
    command=on_generate,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_generate.pack(side=tk.LEFT, padx=5)

button_create_background = tk.Button(
    buttons_frame,
    text="Create Background",
    command=load_background_page,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_create_background.pack(side=tk.LEFT, padx=5)

button_test = tk.Button(
    buttons_frame,
    text="Test",
    command=on_test,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_test.pack(side=tk.LEFT, padx=5)

# Load the main page initially
load_main_page()

# Start the GUI event loop
root.mainloop()
