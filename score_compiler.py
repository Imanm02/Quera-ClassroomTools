import os
import re
import pandas as pd

# Load student IDs from an Excel file
df = pd.read_excel('students.xlsx', header=None)
students = df[0].tolist()

# Walk through directories to find question folders
questions = []
for path, dirs, files in os.walk('.'):
    questions = dirs
    break

# Initialize scores dictionary
scores = {question: {student: 0 for student in students} for question in questions}

# Process each file and extract scores
for path, dirs, files in os.walk('.'):
    if len(path.split('\\')) < 3:
        continue
    _, q, s = path.split('\\')
    try:
        s = int(s)
    except:
        continue
    if s not in students:
        continue
    with open(f'{path}\\result.txt', encoding="utf8") as file:
        res = file.read()
        match = re.search(r'judge score with delay: (\d+)', res)
        if match:
            scores[q][s] = int(match.group(1))

# Convert scores to a DataFrame and join with student IDs
df2 = pd.DataFrame(scores)
df = df.join(df2, on=[0])
df.to_excel('Results.xlsx')