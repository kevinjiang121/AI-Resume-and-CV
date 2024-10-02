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

if __name__ == "__main__":
    experience = read_experience.read_experience("experience.json")
    education = load_education(experience)
    skill = load_skills(experience)
    print(skill) # test render