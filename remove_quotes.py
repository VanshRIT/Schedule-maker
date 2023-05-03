import csv

with open("class_schedule.csv", "r") as file:
    with open("class_updated.csv", "w", newline='') as file_new:
        reader = csv.reader(file);
        writer = csv.writer(file_new);
        writer.writerow(next(reader))
        
        prev = []
        current = []
        for row in reader:
            for i, field in enumerate(row):
                print(prev)
                if "\"" in field:
                    current.append(prev[i])
                    continue;
                current.append(field)
            prev = list(current)
            writer.writerow(current);
            current.clear()
