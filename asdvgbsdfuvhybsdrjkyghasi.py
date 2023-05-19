import csv

with open("class_schedule.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    next(reader)

    dept = {}

    for row in reader:
        if row[0] == row[1] == row[2] == "":
            dept[row[5]] = []
            current_dept = row[5]
            continue

        if row[2] == "\"":
            continue

        if row[2].strip().upper() not in dept[current_dept]:
            dept[current_dept].append(row[2].strip().upper())

# for k, v in dept.items():
#     print(k)
#     for i in v:
#         print(i)
#     print()
