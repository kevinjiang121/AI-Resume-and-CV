# gui.py

import tkinter as tk
from tkinter import messagebox
import renderer  # Ensure renderer.py is in the same directory or adjust the import path accordingly
import threading  # For running API calls in a separate thread
import math  # For trigonometric functions used in the loading animation
import time  # To measure API request duration
import generate_background  # Import the module with background page functions
import generate_cover_letter  # Import the cover letter module

# Global variable to store job description
job_description = ""

def save_job_description():
    """
    Retrieves the text from the Job Description text box and saves it in the global variable.
    """
    global job_description
    job_description = text_job_description.get("1.0", "end-1c").strip()

def on_generate_resume():
    save_job_description()  # Save the job description first

    file_name = entry_filename.get().strip()
    if not file_name:
        messagebox.showwarning("Input Required", "Please enter a file name for the resume.")
        return

    try:
        success = renderer.generate_pdf(file_name)
        if success:
            messagebox.showinfo("Success", f"Resume '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")
    except Exception as e:
        messagebox.showerror("Failure", f"Resume generation failed.\n\n{e}")

def load_main_page():
    for widget in root.winfo_children():
        widget.pack_forget()

    label_filename.pack(pady=(20, 5))
    entry_filename.pack(pady=(0, 10))
    label_job_description.pack(pady=(0, 5))
    text_job_description.pack(pady=(0, 20))
    buttons_frame.pack(pady=(0, 20))

def load_background_page():
    """
    Displays the background information page using functions from generate_background.py.
    """
    save_job_description()  # Save the job description before switching pages

    # Call the function from generate_background module
    generate_background.load_background_page(root, load_main_page)

def load_cover_letter_page():
    """
    Displays the cover letter generation page using functions from generate_cover_letter.py.
    """
    save_job_description()  # Save the job description before switching pages

    # Call the function from generate_cover_letter module
    generate_cover_letter.load_cover_letter_page(root, load_main_page, job_description, entry_filename)

def on_test():
    save_job_description()  # Save the job description first

    if not job_description:
        messagebox.showwarning("Input Required", "Please enter a job description before testing.")
        return

    try:
        renderer.call_openai_assistant(job_description)
        messagebox.showinfo("Success", "OpenAI Assistant has processed your job description.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while calling OpenAI Assistant:\n{e}")

def on_focus_in(event):
    if text_job_description.get("1.0", "end-1c") == "Job Description":
        text_job_description.delete("1.0", "end")
        text_job_description.config(fg="black")

def on_focus_out(event):
    if text_job_description.get("1.0", "end-1c") == "":
        text_job_description.insert("1.0", "Job Description")
        text_job_description.config(fg="grey")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("700x600")
root.resizable(False, False)

# Main page widgets
label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
entry_filename = tk.Entry(root, width=60, font=("Arial", 12))

label_job_description = tk.Label(root, text="Job Description:", font=("Arial", 12))
text_job_description = tk.Text(root, width=60, height=15, font=("Arial", 12), fg="grey")
text_job_description.insert("1.0", "Job Description")
text_job_description.bind("<FocusIn>", on_focus_in)
text_job_description.bind("<FocusOut>", on_focus_out)

buttons_frame = tk.Frame(root)

button_generate_resume = tk.Button(
    buttons_frame,
    text="Generate Resume",
    command=on_generate_resume,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_generate_resume.pack(side=tk.LEFT, padx=5)

button_generate_cover_letter = tk.Button(
    buttons_frame,
    text="Generate Cover Letter",
    command=load_cover_letter_page,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_generate_cover_letter.pack(side=tk.LEFT, padx=5)

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

# Start the application by loading the main page
load_main_page()

# Start the Tkinter event loop
root.mainloop()
