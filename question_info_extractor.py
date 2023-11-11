from bs4 import BeautifulSoup
import requests
import re

session = requests.Session()
cookies = {'session_id': {your_session_id}}
response = session.get('https://quera.org/course/{your_course_id}/', cookies=cookies).text
soup = BeautifulSoup(response, features='html.parser')

# Extract problem set information
problemsets = []
for row in soup.find_all('div', attrs={'class': 'menu'})[0].find_all('a'):
    problemsets.append({'title': row['data-text'].strip(),
                        'link': 'https://quera.org' + row['href'].splitlines()[0].strip()})

# Extract question information from each problem set
for problemset in problemsets:
    response = session.get(problemset['link'], cookies=cookies).text
    soup = BeautifulSoup(response, features='html.parser')
    for q in soup.find_all('a', attrs={'class': 'item problem_menu_item'}):
        params = re.sub(' +', ' ', q.text).splitlines()
        name = params[2].strip()
        score = params[-2].strip()
        print(f"{name}, {problemset['title']}, https://quera.ir{q['href'].splitlines()[0].strip()}, {score}")