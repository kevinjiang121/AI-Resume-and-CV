import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import messagebox, scrolledtext

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
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder '{output_folder}'.\n{e}")
            return False

    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'document.tex')
        
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
    
    latex_content = text_latex.get("1.0", tk.END).strip()
    if not latex_content:
        messagebox.showwarning("Input Required", "Please enter LaTeX content.")
        return
    
    success = latex_to_pdf(latex_content, output_filename=file_name)
    if success:
        messagebox.showinfo("Success", f"PDF '{file_name}' has been generated successfully in 'Resume and Cover Letter' folder.")

root = tk.Tk()
root.title("LaTeX to PDF Generator")
root.geometry("600x500")
root.resizable(False, False)

label_filename = tk.Label(root, text="File Name:", font=("Arial", 12))
label_filename.pack(pady=(20, 5))

entry_filename = tk.Entry(root, width=50, font=("Arial", 12))
entry_filename.pack(pady=(0, 20))

label_latex = tk.Label(root, text="LaTeX Content:", font=("Arial", 12))
label_latex.pack()

text_latex = scrolledtext.ScrolledText(root, width=70, height=20, font=("Courier", 10))
text_latex.pack(pady=(5, 20))

button_generate = tk.Button(root, text="Generate PDF", command=generate_pdf, font=("Arial", 12), bg="green", fg="white")
button_generate.pack(pady=(0, 20))

root.mainloop()
