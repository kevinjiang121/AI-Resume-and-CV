# renderer.py

import os
import subprocess
import tempfile
from jinja2 import Template
from read_experience import read_experience
import load_template
import latexconfig  # Ensure this imports the necessary variables
import chatgpt_api_call  # Import the chatgpt_api_call module

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

    # Escape '#' characters in the LaTeX string
    latex_str = latex_str.replace('#', r'\#')

    # Define the base file name without extension
    base_filename = os.path.splitext(output_filename)[0]
    tex_output_path = os.path.join(output_folder, f"{base_filename}.tex")
    
    # Save the LaTeX string as a .tex file in the output folder
    with open(tex_output_path, 'w', encoding='utf-8') as tex_file:
        tex_file.write(latex_str)

    # Proceed with PDF generation in a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'document.tex')
        
        # Write LaTeX string to temporary .tex file for PDF compilation
        with open(tex_path, 'w', encoding='utf-8') as temp_tex_file:
            temp_tex_file.write(latex_str)
        
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
            print("LaTeX compilation succeeded.")
            print("Output:\n", result.stdout)  # Optional, for successful output logs

        except subprocess.CalledProcessError as e:
            # Print detailed error output
            print("Failed to compile LaTeX document.")
            print("Standard Output:\n", e.stdout)
            print("Error Output:\n", e.stderr)
            raise RuntimeError(f"LaTeX compilation failed. See output above for details.")
        
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
    
    # Path to the LaTeX resume template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'LaTeX Templates', 'resume_template.tex')
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The template file was not found at '{template_path}'.")
    
    # Read experience data
    experience = read_experience("experience.json")
    
    # Define context with variables from latexconfig and rendered sections
    context = {
        'name': latexconfig.name(),
        'email': latexconfig.email(),
        'phonenumber': latexconfig.phonenumber(),
        'github': latexconfig.github(),
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

def generate_cover_letter(file_name, company_name, company_state, company_zipcode, company_city, job_description):
    if not file_name.lower().endswith('.pdf'):
        file_name += '.pdf'
    
    # Path to the LaTeX cover letter template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'LaTeX Templates', 'cover_letter_template.tex')
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"The template file was not found at '{template_path}'.")

    # Read experience data
    experience = read_experience("experience.json")
    
    # Call the assistant with the job description as the prompt
    letter_content = call_openai_assistant(job_description)
    
    # Define context with variables from latexconfig, company info, and letter content
    context = {
        'name': latexconfig.name(),
        'email': latexconfig.email(),
        'phonenumber': latexconfig.phonenumber(),
        'github': latexconfig.github(),
        'companyname': company_name,
        'companystate': company_state,
        'companyaddress': company_city,
        'companyzipcode': company_zipcode,
        'letter': letter_content  # Assistant's response added to context
    }
    
    # Replace placeholders in the template
    final_latex = replace_placeholder(template_path, context)
    
    # Generate PDF
    success = latex_to_pdf(final_latex, output_filename=file_name)
    return success


def call_openai_assistant(prompt):
    """
    Calls the OpenAI assistant with the provided prompt and name.
    Returns the result as a string.
    """
    try:
        if not prompt:
            print("Prompt cannot be empty.")
            return ""

        # Retrieve the name from latexconfig.py
        name = latexconfig.name

        # Call the openai_assistant_call method from chatgpt_api_call.py
        result = chatgpt_api_call.openai_assistant_call(prompt, name)

        # Return the result obtained from the assistant
        return result

    except Exception as e:
        print(f"An error occurred while calling OpenAI Assistant: {e}")
        return ""


if __name__ == "__main__":
    # Here you can call functions to test the functionality
    # For example, to test the call_openai_assistant function:
    generate_cover_letter("Hi5~", "ASD", "ASD", "ASD", "ASD", "Salesforce")