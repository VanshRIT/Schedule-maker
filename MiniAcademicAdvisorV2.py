from MiniAcademicAdvisor import get_priority_value
import dbconfig
import mysql.connector

CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP = {'GCIS 123': 1, 'GCIS 124': 2, 'CSEC 140': 1, 'NSSA 241': 2, 'MATH 181': 1, 'MATH 182': 2, 'MATH 190': 3, 'CSEC 201': 3,
                'CSEC 202': 4, 'NSSA 221': 3, 'NSSA 245': 4, 'MATH 251': 4, 'MATH 241': 5, 'CSCI 462': 5, 'CSEC 380': 6, 'ISTE 230': 5,
                'CSEC 472': 6, 'PUBL 363': 5, "UWRT 150": 1, "YOP 10": 1}


completed_courses = []

csec_courses_stack = sorted(CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP.keys(), key=lambda x: (get_priority_value(x, CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP.keys()) - CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP[x]))
csec_courses_stack = [course for course in csec_courses_stack if course not in completed_courses]


def miniAcademicAdvising(csec_courses_stack, completed_courses, num_courses):
    csec_courses_stack = list(csec_courses_stack)
    db = mysql.connector.connect(
        host=dbconfig.HOST,
        user=dbconfig.USER,
        password=dbconfig.PASSWORD,
        database=dbconfig.DATABASE
    )

    cursor = db.cursor()

    current_sem = [csec_courses_stack.pop() for _ in range(num_courses)]
    while True:
        original_current_sem = list(current_sem)

        for i, course in enumerate(original_current_sem):
            cursor.execute(
                f"SELECT Prerequisites FROM class_updated WHERE subject=\"{course.split()[0]}\" and catalog_number=\"{course.split()[1]}\"")

            prereqs = cursor.fetchall()

            if prereqs:
                prereqs = prereqs[0][0]
            else:
                continue

            if prereqs is None:
                continue

            prereqs = prereqs.split(",")

            prereq_satisfied = False
            prereqs_in_csec_courses = []

            for prereq in prereqs:
                if prereq[-1].isalpha():
                    prereq = prereq[:-1]

                if prereq[0] == '(':
                    prereq = prereq[1:]

                if prereq[-1] == ')':
                    prereq = prereq[:-1]

                if prereq in completed_courses:
                    prereq_satisfied = True
                    break

                if prereq in csec_courses_stack or prereq in current_sem:
                    prereqs_in_csec_courses.append(prereq)

            # Second condition temporary
            if prereq_satisfied or len(prereqs_in_csec_courses) == 0 or course in prereqs_in_csec_courses:
                continue

            prereqs_in_csec_courses.sort(key=lambda x: (get_priority_value(x, CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP.keys()) - CSEC_COURSES_EXPECTED_SEMESTER_OF_TAKING_MAP[x]))
            for prereq in prereqs_in_csec_courses:
                if prereq in current_sem:
                    current_sem[i] = csec_courses_stack.pop()
                    break
            else:
                current_sem[i] = prereqs_in_csec_courses.pop()
                csec_courses_stack.remove(current_sem[i])

        if current_sem == original_current_sem:
            break

    return current_sem

current = miniAcademicAdvising(csec_courses_stack, completed_courses, 5)
print("sem 1 -", current)
completed_courses.extend(current)
csec_courses_stack = [course for course in csec_courses_stack if course not in completed_courses]

for i in range(2):
    current = miniAcademicAdvising(csec_courses_stack, completed_courses, 3)
    print(f"sem {i + 2} -", current)
    completed_courses.extend(current)
    csec_courses_stack = [course for course in csec_courses_stack if course not in completed_courses]


