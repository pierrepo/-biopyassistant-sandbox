""" Script to convert a text file containing questions to a YAML file format.

Usage:
    python src/tools/convert_questions_yaml.py
"""

import yaml
from loguru import logger


# Define the input and output file paths
input_file_path = 'data/banque_questions_python.txt'
output_file_path = 'data/banque_questions_python.yaml'
logger.info(f"Converting questions from {input_file_path} to {output_file_path}...")

# Read the questions from the input file
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Initialize the data structure
data = {'questions': {}}
current_chapter = None
chapter_questions = []
question_counter = 0

# Parse the questions and store them in the data structure
for line in lines:
    line = line.strip()
    if line.startswith('Chapitre'):
        if current_chapter is not None:
            data['questions'][current_chapter] = chapter_questions
        current_chapter = line
        chapter_questions = []
        question_counter = 0
    elif line:
        # Remove the '*' character at the beginning of the line
        if line.startswith('*'):
            line = line[1:].strip()
        question_counter += 1
        question_key = f"Q{question_counter}"
        chapter_questions.append({question_key: line})

# Store the last chapter questions
if current_chapter is not None:
    data['questions'][current_chapter] = chapter_questions

logger.info(f"{len(data['questions'])} chapters and {sum(len(questions) for questions in data['questions'].values())} questions found.")

# Save the questions in the output YAML file
with open(output_file_path, 'w', encoding='utf-8') as yaml_file:
    yaml.dump(data, yaml_file, allow_unicode=True, width=float("inf"), sort_keys=False)

logger.success(f"Questions successfully converted and saved in {output_file_path}.")