from flask import Flask, render_template, request

import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'





@app.route('/')
def index():
    return render_template('index.html')
@app.route('/schedule', methods=['POST'])
def schedule():
    course_count = int(request.form['course-count'])
    courses = []
    for i in range(1, course_count + 1):
        subject = request.form.get(f'course{i}-subject')
        catalog_num = request.form.get(f'course{i}-catalog-num')
        if subject and catalog_num:
            courses.append((subject, catalog_num))
    # Parse CSV file and create list of classes
    classes = {}
    with open('class_schedule.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            if (row[2], row[3]) in courses:
                course_key = row[2] + ' ' + row[3]
                section = row[4]
                days = row[10]
                time_start = row[11]
                time_end = row[12]
                if days and time_start and time_end:
                    time = (days, time_start, time_end)
                    if course_key in classes:
                        classes[course_key].append((section, time))
                    else:
                        classes[course_key] = [(section, time)]

    # Create list of sections with no conflicts
    sections = []
    for course_key, sections_list in classes.items():
        for section1 in sections_list:
            conflict = False
            for section2 in sections:
                if section1[1][0] == section2[1][0] and section1[1][1] < section2[1][2] and section1[1][2] > section2[1][1]:
                    conflict = True
                    break
            if not conflict:
                sections.append((course_key, section1))

    # Render template with list of sections
    return render_template('schedule.html', sections=sections)



if __name__ == "__main__":
    app.run(debug=True)