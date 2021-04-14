import csv
import random
import string

num_falculty = 150
faculty_id = 0

rowList = [['FacultyId', 'LastName', 'FirstName', 'Age']]
for i in range(num_falculty):
    letters = string.ascii_lowercase
    rowList.append([faculty_id, ''.join(random.choice(letters) for i in range(
        10)), ''.join(random.choice(letters) for i in range(10)), random.randint(25, 70)])
    faculty_id += 1
with open('FacultyInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rowList)
