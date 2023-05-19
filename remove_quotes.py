import csv

with open("class_schedule.csv", "r") as file:
    with open("class_updated.csv", "w", newline='') as file_new:
        reader = csv.reader(file)
        writer = csv.writer(file_new)
        next(reader)
        writer.writerow(next(reader)[1:])

        prev = []
        current = []
        for row in reader:
            if row[0] == row[1] == row[2] == "":
                continue

            for i, field in enumerate(row):
                if "\"" in field:
                    current.append(prev[i])
                    continue
                current.append(field)
            prev = list(current)
            final_row = current[1:]
            writer.writerow(final_row)
            current.clear()
