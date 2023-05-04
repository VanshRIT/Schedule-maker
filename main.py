from flask import Flask, render_template, request
import mysql.connector
import dbconfig
from datetime import datetime
import itertools

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sections = schedule()
        return render_template('schedule.html', sections=sections)
    return render_template('index.html')
@app.route('/schedule', methods=['POST'])
def schedule():
    num_courses = int(request.form['course-count'])
    if "friday" in request.form:
        want_friday = False
    else:
        want_friday = True

    courses = []

    for i in range(num_courses):
        subject = request.form[f'course-{i + 1}-subject'].upper()
        cat_num = request.form[f'course-{i + 1}-catalog-num']

        courses.append((subject, cat_num))

    classes = {}
    for course in courses:
        classes[' '.join(course)] = []

    db = mysql.connector.connect(
        host=dbconfig.HOST,
        user=dbconfig.USER,
        password=dbconfig.PASSWORD,
        database=dbconfig.DATABASE
    )

    cursor = db.cursor()

    cursor.execute('SELECT class, subject, cat, sect, days, instructor, time_start, time_end FROM class_updated')

    data = list(cursor.fetchall())

    for row in data:
        if (row[1], row[2]) in courses:
            course = row[1] + ' ' + row[2]
            section = row[3]
            days = row[4]
            instructor = row[5]

            try:
                time_start = datetime.strptime(row[6], '%I:%M %p').time().strftime('%H:%M')
                time_end = datetime.strptime(row[7], '%I:%M %p').time().strftime('%H:%M')
            except():
                continue

            if days and time_start and time_end:
                classes[course].append((course, section, days, time_start, time_end, instructor))

    combos = itertools.product(*classes.values())
    viable_schedules = []

    for combo in combos:
        not_viable = False
        for i, course1 in enumerate(combo):
            for j, course2 in enumerate(combo):
                if not want_friday and ('F' in course1[2] or 'F' in course2[2]):
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

    db.close()

    return render_template('schedule.html', sections=viable_schedules)


if __name__ == '__main__':
    app.run(debug=True)
