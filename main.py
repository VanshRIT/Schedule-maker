from flask import Flask, render_template, request
import csv
import itertools
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    num_courses = int(request.form['course-count'])
    if "friday" in request.form:
        wantfriday = False

    else:
        wantfriday = True
    print(request.form)
    courses = []

    for i in range(num_courses):
        subject = request.form[f'course-{i + 1}-subject'].upper()
        cat_num = request.form[f'course-{i + 1}-catalog-num']

        with open('class_schedule.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            


        courses.append((subject, cat_num))

    classes = {}
    for course in courses:
        classes[' '.join(course)] = []

    with open('class_schedule.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if (row['Subject'], row['Cat#']) in courses:
                course = row['Subject'] + ' ' + row['Cat#']
                section = row['Sect#']
                days = row['Days']
                instructor = row['Instructor']

                try:
                    time_start = datetime.strptime(row['Time Start'], '%I:%M %p').time().strftime('%H:%M')
                    time_end = datetime.strptime(row['Time End'], '%I:%M %p').time().strftime('%H:%M')
                except:
                    continue

                if days and time_start and time_end:
                    classes[course].append((course, section, days, time_start, time_end, instructor))

    combos = itertools.product(*classes.values())
    viable_schedules = []

    for combo in combos:
        not_viable = False
        for i, course1 in enumerate(combo):
            for j, course2 in enumerate(combo):
                if not wantfriday and ('F' in course1[2] or 'F' in course2[2]):
                    not_viable = True
                    break

                if i != j and (course1[2] in course2[2] or course2[2] in course1[2]):
                    if (course1[3] <= course2[3] < course1[4]) or \
                            (course2[3] <= course1[3] < course2[4]) or \
                            (course1[3] <= course2[4] < course1[4]) or \
                            (course2[3] <= course1[4] < course2[4]) or \
                            (course2[3] <= course1[3] and course1[4] <= course2[4]) or \
                            (course1[3] <= course2[3] and course2[4] <= course1[4]):
                        
                            not_viable = True
                            break
            if not_viable:
                break
                    
        if not not_viable:
            viable_schedules.append(combo)

    return render_template('schedule.html', sections=viable_schedules)


if __name__ == "__main__":
    app.run(debug=True)
