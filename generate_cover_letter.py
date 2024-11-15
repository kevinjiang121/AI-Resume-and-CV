# generate_cover_letter.py

import tkinter as tk
from tkinter import messagebox
import threading
import math
import time
import renderer  # Ensure renderer.py is accessible

# Global variables within this module
loading_animation_active = False

# Widgets and variables
entry_company_name = None
entry_company_state = None
entry_company_zipcode = None
entry_company_city = None
loading_canvas = None
job_description = ""
entry_filename = None

def load_cover_letter_page(root, load_main_page, jd, entry_filename_param):
    """
    Displays the cover letter generation page.
    """
    global job_description, entry_filename
    job_description = jd  # Set the module-level job description
    entry_filename = entry_filename_param

    global entry_company_name, entry_company_state, entry_company_zipcode, entry_company_city, loading_canvas

    # Clear the root window
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

    buttons_frame_cover_letter = tk.Frame(root)
    buttons_frame_cover_letter.pack(pady=(20, 10))

    button_back_main = tk.Button(
        buttons_frame_cover_letter,
        text="Back to Main",
        command=load_main_page,
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=18
    )
    button_back_main.pack(side=tk.LEFT, padx=5)

    button_generate_cover_letter = tk.Button(
        buttons_frame_cover_letter,
        text="Generate",
        command=lambda: start_cover_letter_generation(root),
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=18
    )
    button_generate_cover_letter.pack(side=tk.LEFT, padx=5)

    # Loading Animation Canvas
    loading_canvas = tk.Canvas(root, width=100, height=100, highlightthickness=0)
    loading_canvas.pack(pady=(10, 20))

def start_cover_letter_generation(root):
    # Show loading animation
    start_loading_animation(root)

    # Run API request in a separate thread to avoid freezing the GUI
    threading.Thread(target=lambda: on_generate_cover_letter(root)).start()

def start_loading_animation(root):
    global loading_animation_active
    loading_animation_active = True
    rotate_loading_animation(root, 0)

def stop_loading_animation():
    global loading_animation_active
    loading_animation_active = False
    if loading_canvas:
        loading_canvas.delete("all")  # Clear the loading canvas

def rotate_loading_animation(root, angle):
    """
    Displays a circular loading animation with varying shades of gray for a gradient effect.
    """
    if not loading_animation_active:
        return

    if loading_canvas:
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
            color = f"#{shade:02x}{shade:02x}{shade:02x}"
            loading_canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill=color, outline="")

    root.after(100, rotate_loading_animation, root, angle + 30)

def on_generate_cover_letter(root):
    global loading_animation_active, job_description, entry_filename

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
        # Call generate_cover_letter and pass the job_description along with other parameters
        success = renderer.generate_cover_letter(
            file_name, company_name, company_state, company_zipcode, company_city, job_description
        )

        # Print API response code and duration
        duration = time.time() - start_time
        print(f"API Response Successful: {success}, Duration: {duration:.2f} seconds")

        if success:
            messagebox.showinfo(
                "Success",
                f"Cover Letter '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder."
            )
    except Exception as e:
        messagebox.showerror("Failure", f"Cover Letter generation failed.\n\n{e}")
    finally:
        stop_loading_animation()  # Stop loading animation once done
