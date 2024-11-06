# gui.py

import tkinter as tk
from tkinter import messagebox
import renderer  # Ensure renderer.py is in the same directory or adjust the import path accordingly

def on_generate_resume():
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
    for widget in root.winfo_children():
        widget.pack_forget()

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

def load_personal_detail_page():
    global entry_name, entry_email, entry_phone, entry_github

    for widget in root.winfo_children():
        widget.pack_forget()

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

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(20, 10))

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

    button_create_profile = tk.Button(
        buttons_frame,
        text="Create Personal Profile",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=18
    )
    button_create_profile.pack(side=tk.LEFT, padx=5)

def load_cover_letter_page():
    global entry_company_name, entry_company_state, entry_company_zipcode, entry_company_city

    for widget in root.winfo_children():
        widget.pack_forget()

    label_company_name = tk.Label(root, text="Company Name:", font=("Arial", 12))
    label_company_name.pack(pady=(10, 5))
    entry_company_name = tk.Entry(root, width=50, font=("Arial", 12))
    entry_company_name.pack(pady=(0, 10))

    label_company_state = tk.Label(root, text="Company State:", font=("Arial", 12))
    label_company_state.pack(pady=(10, 5))
    entry_company_state = tk.Entry(root, width=50, font=("Arial", 12))
    entry_company_state.pack(pady=(0, 10))

    label_company_zipcode = tk.Label(root, text="Company Zipcode:", font=("Arial", 12))
    label_company_zipcode.pack(pady=(10, 5))
    entry_company_zipcode = tk.Entry(root, width=50, font=("Arial", 12))
    entry_company_zipcode.pack(pady=(0, 10))

    label_company_city = tk.Label(root, text="Company City:", font=("Arial", 12))
    label_company_city.pack(pady=(10, 5))
    entry_company_city = tk.Entry(root, width=50, font=("Arial", 12))
    entry_company_city.pack(pady=(0, 10))

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(20, 10))

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

    button_generate_cover_letter = tk.Button(
        buttons_frame,
        text="Generate",
        command=on_generate_cover_letter,
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=18
    )
    button_generate_cover_letter.pack(side=tk.LEFT, padx=5)

def on_generate_cover_letter():
    file_name = entry_filename.get().strip()
    company_name = entry_company_name.get().strip()
    company_state = entry_company_state.get().strip()
    company_zipcode = entry_company_zipcode.get().strip()
    company_city = entry_company_city.get().strip()

    if not file_name:
        messagebox.showwarning("Input Required", "Please enter a file name for the cover letter.")
        return
    
    try:
        success = renderer.generate_cover_letter(file_name, company_name, company_state, company_zipcode, company_city)
        if success:
            messagebox.showinfo("Success", f"Cover Letter '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")
    except Exception as e:
        messagebox.showerror("Failure", f"Cover Letter generation failed.\n\n{e}")

def on_test():
    prompt = text_job_description.get("1.0", "end-1c").strip()
    if not prompt or prompt == "Job Description":
        messagebox.showwarning("Input Required", "Please enter a job description before testing.")
        return
    
    try:
        renderer.call_openai_assistant(prompt)
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

root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("700x600")
root.resizable(False, False)

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

load_main_page()

root.mainloop()
