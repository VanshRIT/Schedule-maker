import csv

# Get input from user
num_courses = int(input("Enter the number of courses: "))
courses = []
for i in range(num_courses):
    subject = input("Enter the subject of course {}: ".format(i+1)).upper()
    cat_num = input("Enter the catalog number of course {}: ".format(i+1))
    courses.append((subject, cat_num))

# Parse CSV file and create list of classes
classes = []
with open('class_schedule.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    for row in reader:
        if (row[2], row[3]) in courses:
            course = row[2] + ' ' + row[3]
            section = row[4]
            days = row[10]
            time_start = row[11]
            time_end = row[12]
            if days and time_start and time_end:
                time = (days, time_start, time_end)
                classes.append((course, section, time))

# Sort list of classes by time
classes.sort(key=lambda x: x[2])

# Create list of sections with no conflicts
sections = {}
for c in classes:
    valid_section = True
    for s in sections.values():
        if c[0] == s[0] or (c[2][0] == s[2][0] and ((c[2][1] >= s[2][1] and c[2][1] < s[2][2]) or (s[2][1] >= c[2][1] and s[2][1] < c[2][2]))):
            valid_section = False
            break
    if valid_section:
        sections[c[0]] = c

# Output sections
print("Best possible schedule:")
for s in sections.values():
    print(s[0], s[1], s[2][0], s[2][1], s[2][2])
