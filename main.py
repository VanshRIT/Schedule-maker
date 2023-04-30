import csv

def get_courses(num_courses):
    courses = []
    for i in range(num_courses):
        course = input(f"Enter course {i+1}: ")
        courses.append(course)
    return courses

def parse_schedule(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        schedule = {}
        next(reader) # skip the header row
        for row in reader:
            course_key = row[1] + ' ' + row[2]
            section = row[3]
            time = f"{row[9]} {row[10]}-{row[11]}"
            if course_key not in schedule:
                schedule[course_key] = {}
            if section not in schedule[course_key]:
                schedule[course_key][section] = []
            schedule[course_key][section].append(time)
    return schedule


def find_best_schedule(courses, schedule):
    sections = {}
    for course in courses:
        sections[course] = []
        for section in schedule[course]:
            if not any(time in sections[course] for time in schedule[course][section]):
                sections[course].append(section)
    return sections

def print_schedule(sections):
    print("Class schedule:")
    for course in sections:
        print(course)
        for section in sections[course]:
            print(f"Section {section}")
        print()

num_courses = int(input("Enter number of courses: "))
courses = get_courses(num_courses)
schedule = parse_schedule('class_schedule.csv')
#print(schedule)
sections = find_best_schedule(courses, schedule)
print_schedule(sections)
