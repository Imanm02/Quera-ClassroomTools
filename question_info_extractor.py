from bs4 import BeautifulSoup
import requests
import re
import csv

with open('data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    session = requests.Session()
    page_count = 26
    for count in range(1, page_count + 1):
        text = session.get(f"https://quera.org/overview/course/3657/manage/edit_user/?page={count}", cookies= {'session_id': ''}).text
        soup = BeautifulSoup(text, features="html.parser")
        rows = soup.tbody.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            student_id = columns[0].input.get('value')
            if not student_id or not student_id.strip().startswith('400'):
                continue
            data = [student_id, columns[1].text.strip(), columns[2].text.strip()]
            print(data)
            writer.writerow(data)
    f.close()
