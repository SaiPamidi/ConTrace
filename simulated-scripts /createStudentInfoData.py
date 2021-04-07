import csv
import random
import string

num_student = 5000
student_id = 0
rowList = [['StudentId', 'LastName', 'FirstName']]
for i in range(num_student):
    letters = string.ascii_lowercase
    rowList.append([student_id, ''.join(random.choice(letters) for i in range(
        10)), ''.join(random.choice(letters) for i in range(10))])
    student_id += 1
with open('StudentInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rowList)
