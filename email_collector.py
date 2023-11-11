from bs4 import BeautifulSoup
import requests
import csv

# Write extracted data to a CSV file
with open('emails.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    session = requests.Session()

    # Loop through the pages of the class
    for page in range(1, 27):
        response = session.get(f"https://quera.org/overview/course/3657/manage/edit_user/?page={page}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract rows of data
        for row in soup.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                email = columns[2].text.strip()
                writer.writerow([email])
