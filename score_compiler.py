import os
import re
import pandas as pd

df = pd.read_excel('students.xlsx', header=None)
questions = []
students = df[0].tolist()

for path, dirs, files in os.walk('.'):
    questions = dirs
    break
scores = dict([(question, dict([(student, 0) for student in students])) for question in questions])
for i, (path, dirs, files) in enumerate(os.walk('.')):
    if len(path.split('\\')) < 3:
        continue
    _, q, s = path.split('\\')
    try:
        s = int(s)
    except:
        # For those who haven't entered their student number (actually haven't submitted any number)
        pass
    if s not in students:
        continue
    with open(f'{path}\\result.txt', encoding="utf8") as EnteringQueraScores:
        res = EnteringQueraScores.read()
        match = re.search(r'judge score with delay: (\d+)', res)
        if match:
            scores[q][s] = int(match.group(1))
df2 = pd.DataFrame(scores)
df = df.join(df2, on=[0])
df.to_excel('Results.xlsx')