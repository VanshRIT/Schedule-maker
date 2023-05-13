import mysql.connector
import requests

import dbconfig

session = requests.session()

db = mysql.connector.connect(
    host=dbconfig.HOST,
    user=dbconfig.USER,
    password=dbconfig.PASSWORD,
    database=dbconfig.DATABASE
)

cursor = db.cursor()
cursor.execute("SELECT DISTINCT Subject FROM class_updated")
subjects = cursor.fetchall()

cursor.execute('''CREATE TABLE IF NOT EXISTS courses_api_tiger_center
                 (subject VARCHAR(255), enrollmentStatus VARCHAR(255), classType VARCHAR(255), component VARCHAR(255),
                 instructionMode VARCHAR(255), campus VARCHAR(255), term VARCHAR(255), academicGroupShort VARCHAR(255),
                 academicCareer VARCHAR(255), courseTitleLong VARCHAR(255), catalogNumber VARCHAR(255), waitCap INT,
                 classNumber INT UNIQUE, sessionCode VARCHAR(255), waitTotal INT, enrollmentCap INT, ppSearchId VARCHAR(255),
                 academicTitle VARCHAR(255), location VARCHAR(255), enrollmentTotal INT, classSection VARCHAR(255),
                 courseDescription TEXT, academicGroup VARCHAR(255), maximumUnits INT, minimumUnits INT,
                 gradingBasis VARCHAR(255), associatedClassNumber VARCHAR(255), autoEnrollSect1 VARCHAR(255),
                 autoEnrollSect2 VARCHAR(255), courseId VARCHAR(255), printTopic VARCHAR(255),
                 courseTopicId VARCHAR(255), instructorFullName VARCHAR(255), instructorEmail VARCHAR(255),
                 statusImage VARCHAR(255), consent VARCHAR(255))''')

burp0_url = "https://tigercenter.rit.edu:443/tigerCenterApp/tc/class-search"

burp0_json={"searchParams": {"campus": "DUBAI", "career": None, "college": None, "component": None, "courseAttributeOptions": [], "courseAttributeOptionsPassed": [], "creditsMax": None, "creditsMin": None, "filterAnd": True, "instructionType": None, "instructor": None, "isAdvanced": True, "precision": None, "query": "", "session": "DU1", "subject": None, "term": "2231"}}

for subject in subjects:
    burp0_json["searchParams"]["query"] = subject[0]

    rsp = session.post(burp0_url, json=burp0_json)

    for section in rsp.json()["searchResults"]:
        try:
            cursor.execute('INSERT INTO courses VALUES (%s)' % ','.join(['%s'] * len(section.values())),
                           tuple(section.values()))
            cursor.commit()
        except mysql.connector.errors.IntegrityError:
            cursor.rollback()


