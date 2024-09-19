import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

def replace_placeholder(template_str, user_input, placeholder="(Insert Text)"):
    """
    Replaces the placeholder in the template string with the user input.

    Parameters:
    - template_str (str): The LaTeX template as a string.
    - user_input (str): The content to replace the placeholder with.
    - placeholder (str): The placeholder text to be replaced.

    Returns:
    - str: The modified LaTeX string.
    """
    return template_str.replace(placeholder, user_input)

def latex_to_pdf(latex_str, output_filename='output.pdf', output_folder='Resume and Cover Letter'):
    """
    Converts a LaTeX string to a PDF file within a specified folder.

    Parameters:
    - latex_str (str): The LaTeX document as a string.
    - output_filename (str): The desired name for the output PDF file.
    - output_folder (str): The folder where the PDF will be saved.

    Returns:
    - bool: True if PDF is generated successfully, False otherwise.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder '{output_folder}'.\n{e}")
            return False

    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'document.tex')
        
        # Write LaTeX string to .tex file
        try:
            with open(tex_path, 'w', encoding='utf-8') as tex_file:
                tex_file.write(latex_str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write LaTeX content to file.\n{e}")
            return False
        
        # Compile LaTeX to PDF
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Compilation Error", f"Failed to compile LaTeX document.\n\nError Output:\n{e.stderr}")
            return False
        
        # Path to the generated PDF
        generated_pdf = os.path.join(temp_dir, 'document.pdf')
        
        if os.path.exists(generated_pdf):
            destination_pdf = os.path.join(output_folder, output_filename)
            try:
                os.replace(generated_pdf, destination_pdf)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF to '{output_folder}'.\n{e}")
                return False
        else:
            messagebox.showerror("Error", "PDF was not generated. Please check your LaTeX content.")
            return False

def generate_pdf():
    """
    Handler for the Generate button. Retrieves input from the GUI and generates the PDF.
    """
    file_name = entry_filename.get().strip()
    if not file_name:
        messagebox.showwarning("Input Required", "Please enter a file name for the PDF.")
        return
    if not file_name.lower().endswith('.pdf'):
        file_name += '.pdf'
    
    user_content = text_latex.get("1.0", tk.END).strip()
    if not user_content:
        messagebox.showwarning("Input Required", "Please enter content to insert into the LaTeX template.")
        return
    
    # Path to the LaTeX template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'LaTeX Templates', 'testtemplate.txt')
    
    if not os.path.exists(template_path):
        messagebox.showerror("Template Not Found", f"The template file was not found at '{template_path}'.")
        return
    
    # Read the LaTeX template
    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template_str = template_file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the LaTeX template.\n{e}")
        return
    
    # Replace the placeholder with user input
    final_latex = replace_placeholder(template_str, user_content)
    
    # Generate PDF
    success = latex_to_pdf(final_latex, output_filename=file_name)
    if success:
        messagebox.showinfo("Success", f"PDF '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")
    else:
        messagebox.showerror("Failure", "PDF generation failed. Please check your LaTeX content for errors.")

# Setting up the GUI
root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("700x600")
root.resizable(False, False)

# File Name Label and Entry
label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
label_filename.pack(pady=(20, 5))

entry_filename = tk.Entry(root, width=60, font=("Arial", 12))
entry_filename.pack(pady=(0, 20))

# LaTeX Content Label and Text Box
label_latex = tk.Label(root, text="LaTeX Content:", font=("Arial", 12))
label_latex.pack()

text_latex = scrolledtext.ScrolledText(root, width=80, height=25, font=("Courier", 10))
text_latex.pack(pady=(5, 20))

# Generate Button
button_generate = tk.Button(root, text="Generate PDF", command=generate_pdf, font=("Arial", 12), bg="green", fg="white")
button_generate.pack(pady=(0, 20))

# Start the GUI event loop
root.mainloop()
