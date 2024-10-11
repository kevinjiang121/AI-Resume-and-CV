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

# Setting up the GUI
root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("700x200")  # Increased height to accommodate the new button
root.resizable(False, False)

# File Name Label and Entry
label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
label_filename.pack(pady=(20, 5))

entry_filename = tk.Entry(root, width=60, font=("Arial", 12))
entry_filename.pack(pady=(0, 20))

# Generate PDF Button
button_generate = tk.Button(
    root,
    text="Generate PDF",
    command=on_generate,
    font=("Arial", 12),
    bg="green",
    fg="white"
)
button_generate.pack(pady=(0, 10))  # Added some padding below the Generate button

# Create Background Button
button_create_background = tk.Button(
    root,
    text="Create Background",
    command=on_create_background,  # Currently points to a placeholder function
    font=("Arial", 12),
    bg="blue",
    fg="white"
)
button_create_background.pack(pady=(0, 20))  # Added padding below the Create Background button

# Start the GUI event loop
root.mainloop()
