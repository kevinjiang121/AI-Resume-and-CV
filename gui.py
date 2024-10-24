# gui.py

import tkinter as tk
from tkinter import messagebox
import renderer  # Ensure renderer.py is in the same directory or adjust the import path accordingly

def on_generate():
    """
    Handler for the Generate button. Retrieves input from the GUI and generates the PDF.
    """
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

def on_create_background():
    """
    Handler for the Create Background button.
    Currently does nothing but can be implemented in the future.
    """
    messagebox.showinfo("Info", "Create Background button clicked. Functionality to be implemented.")

def on_test():
    """
    Handler for the Test button.
    Retrieves the job description from the text box and passes it to the OpenAI assistant.
    """
    prompt = text_job_description.get("1.0", "end-1c").strip()
    
    # Check if the prompt is empty or still the placeholder
    if not prompt or prompt == "Job Description":
        messagebox.showwarning("Input Required", "Please enter a job description before testing.")
        return
    
    try:
        # Call the OpenAI assistant with the prompt
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
root.geometry("700x600")  # Increased height to accommodate taller text box
root.resizable(False, False)

# File Name Label and Entry
label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
label_filename.pack(pady=(20, 5))

entry_filename = tk.Entry(root, width=60, font=("Arial", 12))
entry_filename.pack(pady=(0, 10))

# Job Description Label and Text Box
label_job_description = tk.Label(root, text="Job Description:", font=("Arial", 12))
label_job_description.pack(pady=(0, 5))

# Increased the height from 5 to 15
text_job_description = tk.Text(root, width=60, height=15, font=("Arial", 12), fg="grey")
text_job_description.pack(pady=(0, 20))

# Insert placeholder text
text_job_description.insert("1.0", "Job Description")

# Bind focus events to handle placeholder text
text_job_description.bind("<FocusIn>", on_focus_in)
text_job_description.bind("<FocusOut>", on_focus_out)

# Buttons Frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=(0, 20))

# Generate PDF Button
button_generate = tk.Button(
    buttons_frame,
    text="Generate PDF",
    command=on_generate,
    font=("Arial", 12),
    bg="green",
    fg="white",
    width=18
)
button_generate.pack(side=tk.LEFT, padx=5)

# Create Background Button
button_create_background = tk.Button(
    buttons_frame,
    text="Create Background",
    command=on_create_background,
    font=("Arial", 12),
    bg="blue",
    fg="white",
    width=18
)
button_create_background.pack(side=tk.LEFT, padx=5)

# Test Button
button_test = tk.Button(
    buttons_frame,
    text="Test",
    command=on_test,
    font=("Arial", 12),
    bg="orange",
    fg="white",
    width=18
)
button_test.pack(side=tk.LEFT, padx=5)

# Start the GUI event loop
root.mainloop()
