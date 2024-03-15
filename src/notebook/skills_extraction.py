import spacy
from spacy.matcher import Matcher
import PyPDF2
import os
import csv

# Load the Spacy English model
nlp = spacy.load('en_core_web_sm')

# Read skills from CSV file
def read_skills_from_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            skills = [row for row in csv_reader]
        return skills[0] if skills else []
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Please provide a valid file path.")
        return []

# Create pattern dictionaries from skills
def create_skill_patterns(skills):
    return [[{'LOWER': skill}] for skill in skills]

# Function to extract skills from text
def extract_skills(text, matcher):
    doc = nlp(text)
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        skills.add(skill)
    return skills

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def skills_extractor(file_path, skills_csv_path):
    # Read skills from CSV file
    skills = read_skills_from_csv(skills_csv_path)
    if not skills:
        return []

    # Create pattern dictionaries from skills
    skill_patterns = create_skill_patterns(skills)

    # Create a Matcher object
    matcher = Matcher(nlp.vocab)

    # Add skill patterns to the matcher
    for pattern in skill_patterns:
        matcher.add('Skills', [pattern])

    # Extract text from PDF
    full_file_path = os.path.join(os.path.dirname(__file__), file_path)
    if not os.path.exists(full_file_path):
        print(f"File '{full_file_path}' not found.")
        return []

    resume_text = extract_text_from_pdf(full_file_path)

    # Extract skills from resume text
    skills = list(extract_skills(resume_text, matcher))
    return skills




