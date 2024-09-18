import os
import subprocess
import tempfile

def latex_to_pdf(latex_str, output_filename='hello_world.pdf', output_folder='Resume and Cover Letter'):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'document.tex')
        
        with open(tex_path, 'w') as tex_file:
            tex_file.write(latex_str)
        
        try:
            subprocess.run(
                ['pdflatex', 'document.tex'],
                cwd=temp_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except subprocess.CalledProcessError:
            print("Failed to compile LaTeX document.")
            return
        
        generated_pdf = os.path.join(temp_dir, 'document.pdf')
        
        if os.path.exists(generated_pdf):
            destination_pdf = os.path.join(output_folder, output_filename)
            os.rename(generated_pdf, destination_pdf)
            print(f"PDF generated successfully: {destination_pdf}")
        else:
            print("Failed to generate PDF.")

if __name__ == "__main__":
    latex_string = r"""
    \documentclass{article}
    \begin{document}
    Hello, World!
    \end{document}
    """
    
    latex_to_pdf(latex_string)
