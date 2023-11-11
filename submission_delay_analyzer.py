import pandas as pd
from unidecode import unidecode
import numpy as np

def read_student_list(path):
    with open(path, "r") as file:
        std_list = file.readlines()
    std_list = [std.strip() for std in std_list]
    std_list.sort(key=lambda item: (len(item), item))
    return std_list

# Define constants and read student list
questions = ["q1"]
keep_grades = []
grade_text = "نمره داوری"
delay_text = "درصد نمره موثر با محاسبه تاخیر"
sid_text = "شناسه کاربری"
std_list = read_student_list("students.txt")
std_set = set(std_list)

# Load Quera output
quera_out = pd.read_excel("assignment_43115_results (1).xlsx")

# Identify columns for grades and delays
grade_index = (quera_out.loc[0,:] == grade_text) | (quera_out.loc[0,:] == sid_text)
late_index = (quera_out.loc[0,:] == delay_text) | (quera_out.loc[0,:] == sid_text)

# Extract relevant data
late_df = quera_out.loc[1:, late_index]
grade_df = quera_out.loc[1:, grade_index]
late_df.columns = ["sid", *[f'q{i}' for i in range(1, late_df.shape[1])]]
grade_df.columns = ["sid", *[f'q{i}' for i in range(1, grade_df.shape[1])]]

# Clean and process data
late_df.sid.fillna("", inplace=True)
late_df.sid = late_df.apply(lambda x: unidecode(x[0]), axis=1)
grade_df.sid.fillna("", inplace=True)
grade_df.sid = grade_df.apply(lambda x: unidecode(x[0]), axis=1)
grade_df_final = grade_df[grade_df.sid.isin(std_set)]
late_df_final = late_df[late_df.sid.isin(std_set)]
grade_df_final.fillna(0, inplace=True)
late_df_final.fillna(0, inplace=True)

# Analyze maximum delay
for q in questions:
    late_df_final[q] = late_df_final[q].astype(np.float32)
final_late = late_df_final.apply(lambda x: pd.Series([x[0], x[1:].max() - 100 if x[1:].max() > 100 else 0],  index=["sid", "late"]), axis=1)

# Prepare final output
final_output = []
for stdn in std_list:
    out = [stdn]
    if stdn in final_late.sid.values:
        out.append(final_late.late[final_late.sid == stdn].values[0])
    else:
        out.append(0)
    if stdn in grade_df_final.sid.values:
        temp_grade = grade_df_final[grade_df_final.sid == stdn]
        for q in keep_grades:
            out.append(float(temp_grade[q].values[0]))
    else:
        for q in keep_grades:
            out.append(0)
    final_output.append(out)

# Save to CSV
pd.DataFrame(final_output, columns=["sid", "late", *keep_grades]).to_csv("out3.csv")
