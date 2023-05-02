from flask import Flask, render_template, request
import csv
import itertools
from datetime import datetime, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    num_courses = int(request.form['course-count'])
    courses = []
    for i in range(num_courses):
        subject = request.form[f'course-{i+1}-subject'].upper()
        cat_num = request.form[f'course-{i+1}-catalog-num']
        courses.append((subject, cat_num))

    classes = {}
    for course in courses:
        classes[course] = []

    with open('class_schedule.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            if (row[2], row[3]) in courses:
                course = row[2] + ' ' + row[3]
                section = row[4]
                days = row[10]
                inst = row[8]

                try:
                    time_start = datetime.strptime(row[11], '%I:%M %p').time().strftime('%H:%M')
                    time_end = datetime.strptime(row[12], '%I:%M %p').time().strftime('%H:%M')
                except:
                    continue

                if days and time_start and time_end:
                    time = (days, time_start, time_end)
                    classes[(row[2], row[3])].append((course, section, time ,inst))
                    print(classes)

    combos = itertools.product(*classes.values())
    no_clash = []

    for combo in combos:
        clash = False
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

    sections = []
    for combo in no_clash:
        section_info = []
        for s in combo:
            section_info.append((s[0], s[1], s[2][0], s[2][1], s[2][2]))
        sections.append(section_info)
        print(sections)

    return render_template('schedule.html', sections=sections)

if __name__ == "__main__":
    app.run(debug=True)