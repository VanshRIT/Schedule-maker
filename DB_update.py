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

if not os.path.exists("SQL"):
    os.makedirs("SQL")
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
query = "SELECT Class, Subject FROM class_updated"
cursor.execute(query)
rows = cursor.fetchall()

class_numbers = [row[0] for row in rows]
subjects = [row[1] for row in rows]

result_dict = {}

for i in range(len(class_numbers)):
    class_num = class_numbers[i]
    subject = subjects[i]
    if class_num in result_dict:
        result_dict[class_num].append(subject)
    else:
        result_dict[class_num] = [subject]

# Iterate over class numbers
for class_number in class_numbers:
    # Find the enrollment for the current class number in JSON data
    subject = result_dict.get(class_number)
    if subject:
        filename = f"Jsons/{subject[0]}.json"
        if filename:
            with open(filename) as file:
                json_data = json.load(file)

            # Find the enrollment for the current class number in JSON data
            enrollment = None
            for result in json_data['searchResults']:
                if result['classNumber'] == str(class_number):  # Convert class_number to str for comparison
                    enrollment = result['enrollmentTotal']
                    cap = result["enrollmentCap"]
                    break

            # Print enrollment for debugging


            # Update the enrollment in the database
            if enrollment is not None:
                update_query = "UPDATE class_updated SET enrollment = %s WHERE Class = %s"
                update_values = (enrollment, class_number)
                cursor.execute(update_query, update_values)

                update_query = "UPDATE class_updated SET enrollment = %s WHERE Class = %s"
                update_values = (cap, class_number)
                cursor.execute(update_query, update_values)
                db.commit()
                print(f"Enrollment updated for class number {class_number}: {enrollment}")
            else:
                print(f"Enrollment not found for class number {class_number}")
        else:
            print(f"Filename not found for subject: {subject[0]}")
    else:
        print(f"Subject not found for class number: {class_number}")

# Close the cursor and connection
cursor.close()
db.close()



