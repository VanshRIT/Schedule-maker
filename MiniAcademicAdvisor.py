import mysql.connector
import dbconfig
from collections.abc import Iterable

# CSEC_COURSES = {"GCIS 123" : False, "GCIS 124" : False, "CSEC 140" : False, "NSSA 241":False, "MATH 181":False, "MATH 182":False, "MATH 190":False, "CSEC 201":False, "CSEC 202":False, "NSSA 221":False, "NSSA 245":False, "MATH 251":False,
#                 "MATH 241" : False, "CSCI 462" : False, "CSEC 380" : False, "ISTE 230":False, "CSEC 472":False, "PUBL 363":False}


def get_priority_value(course: str, CSEC_COURSES: Iterable) -> int:
    # Connect to MySQL
    db = mysql.connector.connect(
        host=dbconfig.HOST,
        user=dbconfig.USER,
        password=dbconfig.PASSWORD,
        database=dbconfig.DATABASE
    )
    cursor = db.cursor()

    prio_value = 0

    for csec_course in CSEC_COURSES:
        if course == csec_course:
            continue

        cursor.execute(f"SELECT Prerequisites FROM class_updated WHERE subject=\"{csec_course.split()[0]}\" and catalog_number=\"{csec_course.split()[1]}\"")
        prereqs = cursor.fetchall()

        if prereqs:
            prereqs = prereqs[0][0]
        else:
            continue

        if prereqs is None:
            continue

        for prereq in prereqs.split(","):
            if prereq[0] == '(':
                prereq = prereq[1:]

            if prereq[-1] == ')':
                prereq = prereq[:-1]

            if course == prereq.strip():
                prio_value += 1 + get_priority_value(csec_course, CSEC_COURSES)
                break

    cursor.close()
    db.close()

    return prio_value
# ................. NOT WORKING BC......................................


if __name__ == "__main__":
    for i in sorted(CSEC_COURSES.keys(), key=lambda x: get_priority_value(x.split()), reverse=True):
        print(i, get_priority_value(i.split()))

    print(sorted(CSEC_COURSES.keys(), key=lambda x: get_priority_value(x.split()), reverse=True))
    sorted_csec = sorted(CSEC_COURSES, key=lambda x: get_priority_value(x.split()), reverse=True)

    count = 0
    current_sem = []
    courses_finished = []

    for course in sorted_csec:
        if not CSEC_COURSES[course]:
            current_sem.append(course)
            count += 1

        if count == 5:
            break


    elimed = []

    def check_prereqs():
        print("changed")
        changed = False
        for i, csec_course in enumerate(current_sem):
            print(csec_course + "...........")
            csec_course = csec_course.split()
            cursor.execute(f"SELECT Prerequisites FROM class_updated WHERE subject=\"{csec_course[0]}\" and catalog_number=\"{csec_course[1]}\"")
            prereqs = cursor.fetchall()

            if prereqs:
                prereqs = prereqs[0][0]
            else:
                continue

            if prereqs is None:
                continue
            b = False
            prereq_in_csec_courses = []
            for prereq in prereqs.split(","):
                print(prereq)
                if prereq[-1].isalpha():
                    prereq = prereq[:-1]

                prereq_in_csec_courses.append(CSEC_COURSES.get(prereq, "False"))

                if CSEC_COURSES.get(prereq, False):
                    b = False
                    break
            else:
                b = True

            if b:
                # if prereq == " ".join(csec_course):
                #     continue

                if prereq_in_csec_courses == ["False"*len(prereq_in_csec_courses)]:
                    continue

                elimed.append(current_sem[i])

                l = False
                print(prereq_in_csec_courses)
                for j, v in enumerate(prereq_in_csec_courses):
                    if type(v) is bool:
                        if prereqs.split(",")[j][-1].isalpha():
                            pass
                        else:
                            prereq = prereqs.split(",")[j]
                            l = True
                if l:
                    continue

                if prereq in current_sem:
                    for course in sorted_csec:
                        if not CSEC_COURSES[course] and course not in current_sem and course not in elimed:
                            current_sem[i] = course
                            break
                else:
                    current_sem[i] = prereq
                print("sadfsadf")
                changed = True
                print(current_sem)

        if changed:
            check_prereqs()

    print(current_sem)
    check_prereqs()
    print(current_sem)



