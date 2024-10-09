# renderer.py

import os
import subprocess
import tempfile
from jinja2 import Template
from read_experience import read_experience
import load_template
import latexconfig  # Ensure this imports the necessary variables

def replace_placeholder(template_path, context):
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        template = Template(template_content)
        rendered_content = template.render(context)
        return rendered_content
    except FileNotFoundError:
        raise FileNotFoundError(f"The template file '{template_path}' was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while rendering the template:\n{e}")

def latex_to_pdf(latex_str, output_filename='output.pdf', output_folder='Resume and Cover Letter'):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'document.tex')
        
        # Write LaTeX string to .tex file
        with open(tex_path, 'w', encoding='utf-8') as tex_file:
            tex_file.write(latex_str)
        
        # Compile LaTeX to PDF
        try:
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'document.tex'],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to compile LaTeX document.\n\nError Output:\n{e.stderr}")
        
        # Path to the generated PDF
        generated_pdf = os.path.join(temp_dir, 'document.pdf')
        
        if os.path.exists(generated_pdf):
            destination_pdf = os.path.join(output_folder, output_filename)
            try:
                os.replace(generated_pdf, destination_pdf)
                return True
            except Exception as e:
                raise RuntimeError(f"Failed to save PDF to '{output_folder}'.\n{e}")
        else:
            raise FileNotFoundError("PDF was not generated. Please check your LaTeX content.")

def generate_pdf(file_name):
    if not file_name.lower().endswith('.pdf'):
        file_name += '.pdf'
    
    # Path to the LaTeX template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'LaTeX Templates', 'resume_template.tex')
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The template file was not found at '{template_path}'.")
    
    # Read experience data
    experience = read_experience("experience.json")
    
    # Define context with variables from latexconfig and rendered sections
    context = {
        'name': latexconfig.name,
        'email': latexconfig.email,
        'phonenumber': latexconfig.phonenumber,
        'github': latexconfig.github,
        'education': load_template.load_education(experience),
        'skills': load_template.load_skills(experience),
        'work_experience': load_template.load_work_experience(experience),
        'projects': load_template.load_project(experience)
    }
    
    # Replace placeholders in the template
    final_latex = replace_placeholder(template_path, context)
    
    # Generate PDF
    success = latex_to_pdf(final_latex, output_filename=file_name)
    return success