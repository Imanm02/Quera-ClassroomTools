# Quera Classroom Tools

## Description

Quera-ClassroomTools is a repository containing a collection of Python scripts designed to automate and simplify the management of educational data on the [Quera platform](https://quera.org/). These tools are aimed at educators and administrators, facilitating tasks such as score compilation, email collection, comprehensive data extraction, question information retrieval, and submission delay analysis.

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

#### Example Usage

To use the Score Compiler, place the `students.xlsx` file in the same directory as the script. This file should contain student IDs in the first column. Also, ensure the question folders are properly organized in the same directory. Then run the script using:

```shell
python score_compiler.py
```

This will generate an `Results.xlsx` file with compiled scores.

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

#### Example Usage

Before running the script, ensure you have the correct URL of the Quera class and the necessary session cookies for access. Use the following command to run the script:

```shell
python email_collector.py
```

The script will create a `data.csv` file containing the email addresses of the students.

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

#### Example Usage

Ensure the script has access to the Quera class page and set the necessary session cookies. Run the script using:

```shell
python data_collector.py
```

This will result in a `data.csv` file with detailed student information.

### 4. Question Info Extractor (`question_info_extractor.py`)
Retrieves detailed information about Quera class questions, such as names, exercise names, links, and scores.

#### Code Walkthrough

This script gathers comprehensive data about students in a Quera class.

- It starts by opening a CSV file to store the extracted data.
- A session is initiated using `requests` to handle HTTP requests, along with the necessary cookies for authentication.
- The script then loops through a specified number of pages (change it for your case).
- For each page, it fetches the HTML content and parses it using `BeautifulSoup`.
- It iterates through each row in the class table, filtering rows based on student IDs.
- For each relevant row, it extracts the student's ID, name, and email, and writes this data to the CSV file.

#### Example Usage

Make sure the script has the correct URL of the Quera course and the session cookies. Execute the script with:

```shell
python question_info_extractor.py
```

The script will print the extracted information to the console.

### 5. Submission Delay Analyzer (`submission_delay_analyzer.py`)
Analyzes submission delays on Quera, correlating them with student IDs and providing insights into submission patterns.

### Code Walkthrough

This script analyzes submission delays for Quera assignments.

- It begins with a function to read a list of student IDs from a file.
- Constants are defined for identifying specific columns in the Quera output.
- The script then loads the Quera results from an Excel file.
- Columns relevant to grades and delays are identified and extracted.
- Data cleaning includes filling missing values and converting student IDs using `unidecode`.
- It then filters the data for relevant students and analyzes the maximum delay for each student.
- The final step is to prepare and output a CSV file, listing each student's ID, maximum delay, and any specified grades.

#### Example Usage

Before running the script, prepare the necessary Excel file containing the Quera assignment results. Then execute the script using:

```shell
python submission_delay_analyzer.py
```

The script will generate a `output.csv` file containing the analysis of submission delays.

### 6. Delay Extractor (`delay_extractor.py`)
Extracts the delay times between assignment deadlines and actual submission times for each student in a Quera course.

#### Code Walkthrough

This script analyzes the time differences between when assignments were due and when they were actually submitted.

- It starts by establishing a session with `requests` to authenticate and access Quera's data.
- Extracts assignment deadlines from each course page using `BeautifulSoup`.
- Iterates over submissions for each assignment, calculating the delay by comparing the submission timestamp to the deadline.
- Stores the results in a dictionary with student IDs as keys and lists of delays as values.
- Outputs the delay data into a CSV file for further analysis or reporting.

#### Example Usage

Ensure that you have configured the necessary session cookies and have access to the Quera course pages. Run the script using:

```shell
python delay_extractor.py
```

This will generate a `delays.csv` file, detailing the submission delays for each student.

## Maintainer

- [Iman Mohammadi](https://github.com/Imanm02)