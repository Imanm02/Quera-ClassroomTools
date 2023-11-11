from bs4 import BeautifulSoup
import requests
import re

session = requests.Session()
cookies = {'session_id': '31jzn0j0xbrtbl48ioab2qoxicr0ls71'}
text = requests.get('https://quera.org/course/6600/', cookies=cookies).text
soup = BeautifulSoup(text, features='html.parser')
rows = soup.find_all('div', attrs={'class': 'menu'})[0].find_all('a')
problemsets = []
for row in rows:
    problemsets.append({'title': row['data-text'].strip(),
                        'link': 'https://quera.org' + row['href'].splitlines()[0].strip()})
for problemset in problemsets:
    text = requests.get(problemset['link'], cookies=cookies).text
    soup = BeautifulSoup(text, features='html.parser')
    qs = soup.find_all('a', attrs={'class': 'item problem_menu_item'})
    for q in qs:
        params = re.sub(' +', ' ', q.text).splitlines()
        name = params[2]
        score = params[-2]
        print(f"{name}, {problemset['title']},  https://quera.ir{q['href'].splitlines()[0].strip()}, کصشر, {score}")
