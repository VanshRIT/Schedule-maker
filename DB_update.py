import requests
import os
import threading
import json
import mysql.connector
import dbconfig


directory = "Jsons/"

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        # Remove the file
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

burp0_url = "https://tigercenter.rit.edu:443/tigerCenterApp/tc/class-search"
values = [
    'ACCT ', 'DECS ', 'FINC ', 'INTB ', 'MGIS ', 'SCBI ', 'MGMT ', 'MKTG ',
    'EGEN ', 'CMPR ', 'EEEE ', 'ISEE ', 'MECE ', 'GCIS ', 'ISTE ', 'NSSA ',
    'SWEN ', 'CSEC ', 'CSCI ', 'PUBL ', 'ANTH ', 'COMM ', 'ECON ', 'ELCA ',
    'ENGL ', 'HIST ', 'MLAR ', 'MLFR ', 'MLSP ', 'PHIL ', 'PSYC ', 'UWRT ',
    'BIOG ', 'BIOL ', 'CHMG ', 'MATH ', 'PHYS ', 'STAT ', 'ACSC ', 'YOPS '
]

burp0_json = {
    "searchParams": {
        "campus": "DUBAI",
        "career": None,
        "college": None,
        "component": None,
        "courseAttributeOptions": [],
        "courseAttributeOptionsPassed": [],
        "creditsMax": None,
        "creditsMin": None,
        "filterAnd": True,
        "instructionType": None,
        "instructor": None,
        "isAdvanced": True,
        "precision": None,
        "query": "",
        "session": "DU1",
        "subject": None,
        "term": "2231"
    }
}

if not os.path.exists("Jsons"):
    os.makedirs("Jsons")


def export_json(value):
    burp0_json["searchParams"]["query"] = value.strip()

    resp = requests.post(burp0_url, json=burp0_json)
    obj = json.loads(resp.text)

    json_filename = f"Jsons/{value.strip()}.json"

    with open(json_filename, "w") as file:
        json.dump(obj, file)

    print("Data exported to:", json_filename)


# Export JSON files
threads = []
for value in values:
    t = threading.Thread(target=export_json, args=(value,))
    threads.append(t)
    t.start()

# Wait for all export threads to complete
for t in threads:
    t.join()

print("JSON files creation completed.")

# Connect to MySQL
db = mysql.connector.connect(
    host=dbconfig.HOST,
    user=dbconfig.USER,
    password=dbconfig.PASSWORD,
    database=dbconfig.DATABASE
)
cursor = db.cursor()

# Retrieve class numbers from the database
query = "SELECT Class_Number, Subject FROM class_updated"
cursor.execute(query)
rows = cursor.fetchall()

class_numbers = [row[0] for row in rows]
subjects = [row[1] for row in rows]

result_dict = {}

for i in range(len(class_numbers)):
    class_num = class_numbers[i]
    subject = subjects[i]

    if class_num is None:
        continue

    result_dict[class_num] = subject

# Iterate over class numbers
for class_number in class_numbers:
    if class_number is None:
        continue

    subject = result_dict.get(class_number)

    filename = f"Jsons/{subject.strip()}.json"

    with open(filename) as file:
        json_data = json.load(file)

    # Find the enrollment and prereqs for the current class number in JSON data
    enrollment = None
    prereqs = []
    for result in json_data['searchResults']:
        if result['classNumber'] == str(class_number):  # Convert class_number to str for comparison
            enrollment = result['enrollmentTotal']

            if not result["preReqDescrsLong"][0]:
                break

            for word in result["preReqDescrsLong"][0].split():
                if "-" not in word:
                    continue

                if word.split("-")[1] and word.split("-")[1][0].isnumeric():
                    prereqs.append(" ".join(word.split("-")))

    # Update the enrollment in the database
    if enrollment:
        update_query = "UPDATE class_updated SET enrollment = %s WHERE Class_Number = %s"
        update_values = (enrollment, class_number)
        cursor.execute(update_query, update_values)

        print(f"Enrollment updated for class number {class_number}: {enrollment}")
    else:
        print(f"Enrollment not found for class number {class_number}")

    if prereqs:
        update_query = "UPDATE class_updated SET Prerequisites = %s WHERE Class_Number = %s"
        update_values = (",".join(prereqs), class_number)
        cursor.execute(update_query, update_values)
        print(",".join(prereqs))
        print(f"Prerequisites updated for class number {class_number}: {enrollment}")
    else:
        print(f"Prerequisites not found for class number {class_number}")

    db.commit()

# Close the cursor and connection
cursor.close()
db.close()



