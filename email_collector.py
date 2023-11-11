from bs4 import BeautifulSoup
import requests
import csv

# Open CSV file to write emails
with open('data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    session = requests.Session()
    page_count = 26

    # Iterate through each page of the course
    for count in range(1, page_count + 1):
        response = session.get(f"https://quera.org/overview/course/3657/manage/edit_user/?page={count}", cookies={'session_id': ''}).text
        soup = BeautifulSoup(response, features="html.parser")
        
        # Extract and write student emails
        for row in soup.tbody.find_all('tr'):
            columns = row.find_all('td')
            student_id = columns[0].input.get('value')
            if not student_id or not student_id.strip().startswith('400'):
                continue
            email = columns[2].text.strip()
            writer.writerow([email])
