# Course Scheduler

The Course Scheduler is a Python Flask application that generates possible schedules based on user input. The application reads a CSV file containing information about courses and filters them based on user selection. The generated schedules are combinations of courses that don't conflict with each other. 

## Prerequisites

Before running the Course Scheduler, ensure that the following are installed:

- Python 3.x
- Flask
- CSV

## Installation

To install and run the Course Scheduler, follow these steps:

1. Clone this repository.
2. Open your terminal and navigate to the project directory.
3. Run `pip install -r requirements.txt` to install the required packages.
4. Run `python app.py` to start the application.

## Usage

To use the Course Scheduler, follow these steps:

1. Open your browser and navigate to `http://localhost:5000/`.
2. Enter the number of courses you want to schedule and the details of each course.
3. Select whether or not you want courses on Fridays.
4. Click the "Submit" button.
5. The application will generate a list of possible schedules based on the courses selected.

## How it works

When the user inputs the details of the courses they want to schedule, the Course Scheduler reads a CSV file containing information about all available courses. The application filters the available courses based on the user input and generates all possible combinations of courses that don't conflict with each other. The application then displays a list of viable schedules to the user.

## Acknowledgements

The Course Scheduler was created by Vansh Purohit(CS Major) and Pranav Arun(CSEC Major). The inspiration for this project came from a issue we faced almost every time we had to go and select the courses for our semesters.