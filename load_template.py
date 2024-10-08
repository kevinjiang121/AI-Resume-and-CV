import read_experience
from jinja2 import Template
import os

def load_education(experience):
    education = experience['education'][0]
    with open(os.path.join('LaTeX Templates', 'education.tex')) as file:
        template = Template(file.read())
    rendered = template.render(
        university=education['university'],
        universitywebsite=education['university website'],
        major=education['major'],
        enddate=education['end date'],
        minor=education['minor']
    )
    return rendered

def load_skills(experience):
    skills = experience['skills'][0]
    template_path = os.path.join('LaTeX Templates', 'skills.tex')
    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    rendered = template.render(
        skills=skills
    )
    return rendered

def load_project(experience):
    projects = experience.get('projects', [])
    template_path = os.path.join('LaTeX Templates', 'projects.tex')
    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    rendered = template.render(projects=projects)
    return rendered

def load_work_experience(experience):
    work_experiences = experience.get('work experience', [])
    template_path = os.path.join('LaTeX Templates', 'work_experience.tex')
    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    rendered = template.render(work_experience=work_experiences)
    return rendered

if __name__ == "__main__":
    experience = read_experience.read_experience("experience.json")
    education = load_education(experience)
    skill = load_skills(experience)
    work_experience = load_work_experience(experience)
    project = load_project(experience)
    print(project) # test render