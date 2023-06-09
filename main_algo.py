# Original Algorithm that was developed to check for time clashes and give a schedule made to work in the console

import csv
import itertools
from datetime import datetime

# Get input from user
num_courses = int(input("Enter the number of courses: "))
courses = []
for i in range(num_courses):
    subject = input("Enter the subject of course {}: ".format(i + 1)).upper()
    cat_num = input("Enter the catalog number of course {}: ".format(i + 1))
    courses.append((subject, cat_num))

# Parse CSV file and create dictionary with courses as keys and an empty list as value to segregate sections from CSV
classes = {}

for course in courses:
    classes[course] = []

# Loops through rows in the CSV and appends each section to their respective lists in the classes dictionary
with open('class_schedule.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row

    for row in reader:
        if (row[2], row[3]) in courses:
            course = row[2] + ' ' + row[3]
            section = row[4]
            days = row[10]

            # Stores the times as datetime.time objects rather than strings
            try:
                time_start = datetime.strptime(row[11], '%I:%M %p').time().strftime('%H:%M')
                time_end = datetime.strptime(row[12], '%I:%M %p').time().strftime('%H:%M')
            except AttributeError:
                continue

            # To make sure they are not empty values
            if days and time_start and time_end:
                time = (days, time_start, time_end)
                classes[(row[2], row[3])].append((course, section, time))

# Storing all the possible combinations of sections i.e. schedules in combos
combos = itertools.product(*classes.values())
no_clash = []

for combo in combos:
    clash = False  # Flag to check if combo is viable or not

    for i, course1 in enumerate(combo):
        for j, course2 in enumerate(combo):
            if i != j and (course1[2][0] in course2[2][0] or course1[2][0] in course2[2][0]):
                if (course1[2][1] <= course2[2][1] < course1[2][2]) or (
                        course2[2][1] <= course1[2][1] < course2[2][2]) or \
                        (course1[2][1] <= course2[2][2] < course1[2][2]) or (
                        course2[2][1] <= course1[2][2] < course2[2][2]) or \
                        (course2[2][1] <= course1[2][1] and course1[2][2] <= course2[2][2]) or \
                        (course1[2][1] <= course2[2][1] and course2[2][2] <= course1[2][2]):
                    clash = True

    if not clash:
        no_clash.append(combo)

# Output section
print("Best possible schedule:")
for combo in no_clash:
    for s in combo:
        print(s[0], s[1], s[2][0], s[2][1], s[2][2])
    print("\n\n")