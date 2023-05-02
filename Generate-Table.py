import csv
import matplotlib.pyplot as plt
import numpy as np

# read the csv file
with open('class_schedule.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# get input from user
num_courses = int(input("Enter the number of courses: "))
courses = []
for i in range(num_courses):
    course = {}
    course['subject'] = input("Enter the subject of course {}: ".format(i+1))
    course['category'] = input("Enter the category of course {}: ".format(i+1))
    course['section'] = input("Enter the section of course {}: ".format(i+1))
    courses.append(course)

# extract days and times for each course
course_times = []
for course in courses:
    for row in data:
        if row['Subject'] == course['subject'] and row['Cat#'] == course['category'] and row['Sect#'] == course['section']:
            course_time = {}
            days_str = row['Days']
            if 'MWF' in days_str:
                course_time['days'] = 'MWF'
            elif 'MW' in days_str:
                course_time['days'] = 'MW'
            elif 'TR' in days_str:
                course_time['days'] = 'TR'
            else:
                course_time['days'] = days_str
            course_time['time_start'] = row['Time Start']
            course_time['time_end'] = row['Time End']
            course_times.append(course_time)

# create timetable image
days = ['M', 'T', 'W', 'Th', 'F']  # days of the week
times = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']  # times of the day
timetable = np.zeros((len(times), len(days)))  # initialize timetable array
for course_time in course_times:
    days_list = list(course_time['days'])
    for day in days_list:
        day_index = days.index(day)
        time_start = times.index(course_time['time_start'])
        time_end = times.index(course_time['time_end'])
        timetable[time_start:time_end, day_index] = 1  # mark the corresponding times and days as busy

# plot timetable image
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(timetable, cmap='binary', interpolation='nearest', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(np.arange(len(days)))
ax.set_xticklabels(days)
ax.set_yticks(np.arange(len(times)))
ax.set_yticklabels(times)
ax.set_xlabel('Days')
ax.set_ylabel('Time')
ax.set_title('Timetable')
plt.show()
