# gui.py

import tkinter as tk
from tkinter import messagebox
import renderer  # Ensure renderer.py is in the same directory or adjust the import path accordingly
import threading  # For running API calls in a separate thread
import math  # For trigonometric functions used in the loading animation
import time  # To measure API request duration

# Global variable to store job description
job_description = ""
loading_animation_active = False  # Global variable to control the loading animation

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
    Placeholder function for the background page.
    """
    save_job_description()  # Save the job description before switching pages

    for widget in root.winfo_children():
        widget.pack_forget()

    label_background_info = tk.Label(root, text="Background Information Page", font=("Arial", 16))
    label_background_info.pack(pady=(20, 20))

    button_back_main = tk.Button(
        root,
        text="Back to Main",
        command=load_main_page,
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=18
    )
    button_back_main.pack(pady=(20, 20))

def load_cover_letter_page():
    save_job_description()  # Save the job description before switching pages

    global entry_company_name, entry_company_state, entry_company_zipcode, entry_company_city, loading_canvas

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
        command=start_cover_letter_generation,
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=18
    )
    button_generate_cover_letter.pack(side=tk.LEFT, padx=5)

    # Loading Animation Canvas with default background color
    loading_canvas = tk.Canvas(root, width=100, height=100, highlightthickness=0)
    loading_canvas.pack(pady=(10, 20))

def start_cover_letter_generation():
    # Save job description
    save_job_description()
    
    # Show loading animation
    start_loading_animation()

    # Run API request in a separate thread to avoid freezing the GUI
    threading.Thread(target=on_generate_cover_letter).start()

def start_loading_animation():
    global loading_animation_active
    loading_animation_active = True
    rotate_loading_animation(0)

def stop_loading_animation():
    global loading_animation_active
    loading_animation_active = False
    loading_canvas.delete("all")  # Clear the loading canvas

def rotate_loading_animation(angle):
    """
    Displays a circular loading animation with varying shades of gray for a gradient effect.
    """
    if not loading_animation_active:
        return

    loading_canvas.delete("all")  # Clear the canvas

    # Draw dots in a circular pattern
    num_dots = 12
    radius = 40
    dot_radius = 5

    for i in range(num_dots):
        theta = (angle + i * (360 / num_dots)) * math.pi / 180  # Convert to radians
        x = 50 + radius * math.cos(theta)
        y = 50 + radius * math.sin(theta)
        # Generate a shade of gray based on position in the cycle
        shade = 255 - int((i / num_dots) * 200)
        color = f"#{shade:02x}{shade:02x}{shade:02x}"  # Grayscale color without transparency
        loading_canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill=color, outline="")

    root.after(100, rotate_loading_animation, angle + 30)  # Rotate by 30 degrees for the next frame

def on_generate_cover_letter():
    global loading_animation_active

    # Capture start time
    start_time = time.time()

    file_name = entry_filename.get().strip()
    company_name = entry_company_name.get().strip()
    company_state = entry_company_state.get().strip()
    company_zipcode = entry_company_zipcode.get().strip()
    company_city = entry_company_city.get().strip()

    if not file_name:
        messagebox.showwarning("Input Required", "Please enter a file name for the cover letter.")
        stop_loading_animation()
        return
    
    try:
        # Call generate_cover_letter and pass the job_description string along with other parameters
        success = renderer.generate_cover_letter(file_name, company_name, company_state, company_zipcode, company_city, job_description)
        
        # Print API response code and duration
        duration = time.time() - start_time
        print(f"API Response Successful: {success}, Duration: {duration:.2f} seconds")

        if success:
            messagebox.showinfo("Success", f"Cover Letter '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")
    except Exception as e:
        messagebox.showerror("Failure", f"Cover Letter generation failed.\n\n{e}")
    finally:
        stop_loading_animation()  # Stop loading animation once done

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
