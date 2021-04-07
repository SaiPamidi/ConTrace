import csv
import random
import string

"""data = [['CourseId', 'CourseName', 'Units']]
fp = open('coursesRawData.txt', 'r')

for line in fp:
    line = line.strip().split('.')
    data.append([line[0], line[1],
                 line[2][0]])"""

numCourse = 150
courseId = 1
rowList = [['CourseId', 'CourseName']]
for i in range(numCourse+1):
    letters = string.ascii_lowercase
    rowList.append([courseId, ''.join(random.choice(letters) for i in range(
        10))])
    courseId += 1

with open('CourseInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rowList)
