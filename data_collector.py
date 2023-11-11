from bs4 import BeautifulSoup
import requests
import csv

# Prepare to write to a CSV file
with open('data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    session = requests.Session()
    page_count = 26  # Total number of pages to scrape

    # Loop through each page
    for count in range(1, page_count + 1):
        # Fetch the page content
        text = session.get(f"https://quera.org/overview/course/3657/manage/edit_user/?page={count}", cookies={'session_id': '47n484icce2onlj0zge5tvjffth5lbxq'}).text
        soup = BeautifulSoup(text, features="html.parser")
        
        # Process each row in the table
        for row in soup.tbody.find_all('tr'):
            columns = row.find_all('td')
            student_id = columns[0].input.get('value')

            # Filter out irrelevant rows
            if not student_id or not student_id.strip().startswith('400'):
                continue

            # Extract student data and write to file
            data = [student_id, columns[1].text.strip(), columns[2].text.strip()]
            writer.writerow(data)
