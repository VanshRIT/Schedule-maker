import os

from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
import dbconfig
from datetime import datetime
import itertools

app = Flask(__name__)

db = mysql.connector.connect(
    host=dbconfig.HOST,
    user=dbconfig.USER,
    password=dbconfig.PASSWORD,
    database=dbconfig.DATABASE
)


@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = db.cursor()
    cursor.execute('SELECT DISTINCT subject, cat FROM class_updated')
    courses = cursor.fetchall()

    if request.method == 'POST':
        sections = schedule()
        return render_template('schedule.html', sections=sections)

    return render_template('index.html', courses=courses)


@app.route('/instructors')
def instructors():
    selected_course = request.args.get('course')

    cursor = db.cursor()

    cursor.execute('SELECT DISTINCT instructor FROM class_updated WHERE subject = %s AND cat = %s', selected_course.split('-'))

    data = cursor.fetchall()

    instructors_ = [row[0] for row in data]
    instructors_.insert(0, "Any")
    return jsonify(instructors_)


@app.route('/schedule', methods=['POST'])
def schedule():
    num_courses = int(request.form['course-count'])

    if "friday" in request.form:
        want_friday = False
    else:
        want_friday = True

    courses = []

    for i in range(num_courses):
        subject, cat_num = request.form[f'course-{i + 1}-course'].upper().split('-')
        instructor = request.form[f'course-{i + 1}-instructor']

        if instructor.lower() == "any":
            courses.append((subject, cat_num))
        else:
            courses.append((subject, cat_num, instructor))

    viable_schedules = get_viable_schedules(want_friday, get_all_combinations(courses, want_friday))

    return render_template('schedule.html', sections=viable_schedules)


def check_time_clash(combo: tuple) -> bool:
    for i, course1 in enumerate(combo):
        for j, course2 in enumerate(combo):
            if i != j and (course1[2] in course2[2] or course2[2] in course1[2]):
                if (course1[3] <= course2[3] < course1[4]) or \
                    (course2[3] <= course1[3] < course2[4]) or \
                    (course1[3] <= course2[4] < course1[4]) or \
                    (course2[3] <= course1[4] < course2[4]) or \
                    (course2[3] <= course1[3] and course1[4] <= course2[4]) or \
                    (course1[3] <= course2[3] and course2[4] <= course1[4]):
                    return True
            return False


def get_all_combinations(courses, want_friday: bool):
    classes = {}
    classes_with_labs = {}
    cursor = db.cursor()
    cursor.execute("SELECT distinct Subject, Cat from class_updated where sect like \"%L%\"")
    labs_data = cursor.fetchall()

    for course in courses:
        classes[(course[0], course[1])] = []
        has_lab = False

        if (course[0], course[1]) in labs_data:
            has_lab = True
            temp_sections = []
            temp_labs = []

        if len(course) == 2:
            cursor.execute(f'SELECT class, subject, cat, sect, days, instructor, time_start, time_end '
                           f'FROM class_updated WHERE subject="{course[0]}" and cat="{course[1]}"')
        else:
            cursor.execute(f'SELECT class, subject, cat, sect, days, instructor, time_start, time_end '
                           f'FROM class_updated WHERE subject="{course[0]}" and cat="{course[1]}" '
                           f'and instructor="{course[2]}"')

        data = list(cursor.fetchall())

        for row in data:
            course_name = row[1] + ' ' + row[2]
            section = row[3]
            days = row[4]
            instructor = row[5]

            if row[6] is None or row[7] is None:
                continue

            time_start = datetime.strptime(row[6], '%I:%M %p').time().strftime('%H:%M')
            time_end = datetime.strptime(row[7], '%I:%M %p').time().strftime('%H:%M')

            if not (days and time_start and time_end and section):
                return

            if has_lab:
                if "L" in section:
                    temp_labs.append((course_name, section, days, time_start, time_end, instructor))
                else:
                    temp_sections.append((course_name, section, days, time_start, time_end, instructor))

            else:
                classes[(course[0], course[1])].append((course_name, section, days, time_start, time_end, instructor))

        if has_lab:
            classes[(course[0], course[1])] = list(itertools.product(temp_labs, temp_sections))

    return itertools.product(*classes.values())


def get_viable_schedules(want_friday: bool, combos) -> list:
    viable_schedules = []

    for combo in combos:
        not_viable = False

        temp_combo = []
       
        for v in combo:
            if type(v[1]) is tuple:
                temp_combo.extend(v)
            else:
                temp_combo.append(v)

        combo = tuple(temp_combo)

        for course in combo:
            if not want_friday and 'F' in course[2]:
                not_viable = True
                
                break
        if not_viable:
            continue
        
        not_viable = check_time_clash(combo)
       
        if not not_viable:
            viable_schedules.append(combo)

    return viable_schedules




if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))