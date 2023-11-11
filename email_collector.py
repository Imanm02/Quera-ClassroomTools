from bs4 import BeautifulSoup
import requests
import csv

# Write extracted data to a CSV file
with open('emails.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    session = requests.Session()
    class_id = 'your-class-id-here'

    # Loop through the pages of the class
    for page in range(1, 'number-of-pages-here'):
        response = session.get(f"https://quera.org/overview/course/{class_id}/manage/edit_user/?page={page}", cookies= {'session_id': '{your-session-id-here}'}).text
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.tbody.find_all('tr')

        # Extract rows of data
        for row in rows:
            columns = row.find_all('td')
            if columns:
                email = columns[2].text.strip()
                writer.writerow([email])
    f.close()