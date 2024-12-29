import os
import time
import datetime
import jdatetime
import math
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from dotenv import load_dotenv
import argparse

def convert_persian_to_english_digits(persian_number):
    translation_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    return int(persian_number.translate(translation_table))

def fetch_assignment_deadline(assignment_id):
    session_cookie = os.getenv("QUERA_SESSION_ID")
    headers = {'cookie': f'session_id={session_cookie}'}
    endpoint = f"https://quera.org/course/assignments/{assignment_id}/edit"

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return

    page_content = BeautifulSoup(response.text, 'lxml')
    deadline_input = page_content.find('input', {'id': 'id_finish_time'}).get('value')
    deadline_datetime = datetime.datetime.strptime(deadline_input, '%Y/%m/%d %H:%M:%S')
    return jdatetime.datetime.fromgregorian(datetime=deadline_datetime)

def fetch_submissions(assignment_id, deadline):
    session_cookie = os.getenv("QUERA_SESSION_ID")
    headers = {'cookie': f'session_id={session_cookie}'}
    base_url = f"https://quera.org/course/assignments/{assignment_id}/submissions/final"
    student_delays = {}
    unique_problems = set()

    total_pages = 1
    for current_page in range(1, total_pages + 1):
        page_url = f"{base_url}?page={current_page}"
        try:
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            continue

        content = BeautifulSoup(response.text, 'lxml')
        if current_page == 1:
            total_submissions = fetch_total_submissions(content)
            total_pages = calculate_total_pages(total_submissions)
            progress_bar = tqdm(total=total_submissions)

        process_submissions(content, student_delays, unique_problems, deadline, progress_bar)
        time.sleep(1)  # Respectful crawling

    progress_bar.close()
    return student_delays, unique_problems

def fetch_total_submissions(content):
    footer = content.find('tfoot')
    if footer:
        total_text = footer.find('th').text.strip().split(' ')[0]
        return convert_persian_to_english_digits(total_text)
    return len(content.find('tbody').find_all('tr'))

def calculate_total_pages(submissions_count, per_page=20):
    return math.ceil(submissions_count / per_page)

def process_submissions(content, delays, problems, deadline, progress_bar):
    rows = content.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        student_id = extract_student_id(cells)
        problem_id = extract_problem_id(cells)
        submission_time = parse_submission_time(cells)
        update_delays(delays, problems, student_id, problem_id, submission_time, deadline)
        progress_bar.update(1)

def extract_student_id(cells):
    return cells[0].text.strip()

def extract_problem_id(cells):
    return int(cells[2].find('a')['href'].split('/')[-1])

def parse_submission_time(cells):
    date_parts = cells[3].text.strip().split(' ')
    return jdatetime.datetime(
        convert_persian_to_english_digits(date_parts[2]),  # Year
        date_parts[1],  # Month (as name, converted to number in update_delays)
        convert_persian_to_english_digits(date_parts[0]),  # Day
        *map(convert_persian_to_english_digits, date_parts[5].split(':'))  # Hour, Minute
    )

def update_delays(delays, problems, student_id, problem_id, submission, deadline):
    if student_id not in delays:
        delays[student_id] = {}
    problems.add(problem_id)
    if submission > deadline:
        delay_duration = (submission - deadline).total_seconds() / 60  # Convert to minutes
        delays[student_id][problem_id] = delay_duration

if __name__ == "__main__":
    load_dotenv('../.env')
    cli_parser = argparse.ArgumentParser(description='Quera Homework Submission Tracker')
    cli_parser.add_argument('assignment_id', type=int, help='Assignment ID from URL')
    cli_args = cli_parser.parse_args()

    assignment_deadline = fetch_assignment_deadline(cli_args.assignment_id)
    print(assignment_deadline)
    submission_delays, problems_encountered = fetch_submissions(cli_args.assignment_id, assignment_deadline)
    print(problems_encountered)
    print(submission_delays)

    with open(f'{cli_args.assignment_id}.csv', 'w') as file:
        file.write('Student ID,' + ','.join(f'Problem {p}' for p in problems_encountered) + '\n')
        for student, delays in submission_delays.items():
            file.write(f'{student},')
            file.write(','.join(str(delays.get(p, 0)) for p in problems_encountered))
            file.write('\n')