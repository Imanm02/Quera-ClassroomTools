# Quera Classroom Tools

## Description

QueraClassroomTools is a repository containing a collection of Python scripts designed to automate and simplify the management of educational data on the Quera platform. These tools are aimed at educators and administrators, facilitating tasks such as score compilation, email collection, comprehensive data extraction, question information retrieval, and submission delay analysis.

## Scripts

### 1. Score Compiler (`score_compiler.py`)
Compiles student scores from Quera submissions. Takes an input Excel file with student IDs and outputs scores alongside these IDs.

#### Code Walkthrough

This script compiles student scores from Quera exercises.

- It starts by reading student IDs from an Excel file using `pandas`.
- Initializes data structures for storing questions and scores.
- Walks through the directory structure to find folders for each question.
- Prepares a dictionary to store scores, initializing each student's score for each question as 0.
- Processes the result files in each directory, extracting scores using regular expressions.
- Converts the scores dictionary to a DataFrame and joins it with the original DataFrame containing student IDs.
- Finally, outputs the compiled scores to a new Excel file.

### 2. Email Collector (`email_collector.py`)
Extracts and collects email addresses of students from a specific Quera class, saving the data in a CSV file.

#### Code Walkthrough

This script collects email addresses of students enrolled in a specific Quera class.

- It opens a CSV file for writing the collected email addresses.
- Establishes a session with `requests` to handle HTTP requests.
- Loops through a specified number of pages (here, 26 pages).
- Fetches the HTML content of each page and parses it using `BeautifulSoup`.
- Iterates through each row in the class table.
- Filters out rows without valid student IDs or those not starting with '400'.
- Extracts the email from the relevant column and writes it to the CSV file.

### 3. Data Collector (`data_collector.py`)
Gathers comprehensive information about students in a Quera class, including IDs, emails, and names, and organizes it into a CSV file.

#### Code Walkthrough

This script fetches detailed information about questions from a Quera course.

- Initiates a `requests` session with specific cookies for authentication.
- Retrieves the main course page and parses it using `BeautifulSoup`.
- Extracts links to each problem set.
- Iterates through each problem set, fetching its page and parsing it.
- For each question in the problem set, extracts details like the question name, exercise name, link, and score.
- Prints the collected information in a formatted manner.

### 4. Question Info Extractor (`question_info_extractor.py`)
Retrieves detailed information about Quera class questions, such as names, exercise names, links, and scores.

### Data Collector (`data_collector.py`)

This script gathers comprehensive data about students in a Quera class.

- It starts by opening a CSV file to store the extracted data.
- A session is initiated using `requests` to handle HTTP requests, along with the necessary cookies for authentication.
- The script then loops through a specified number of pages (26 in this case).
- For each page, it fetches the HTML content and parses it using `BeautifulSoup`.
- It iterates through each row in the class table, filtering rows based on student IDs.
- For each relevant row, it extracts the student's ID, name, and email, and writes this data to the CSV file.


### 5. Submission Delay Analyzer (`submission_delay_analyzer.py`)
Analyzes submission delays on Quera, correlating them with student IDs and providing insights into submission patterns.

## Maintainer

- [Iman Mohammadi](https://github.com/Imanm02)