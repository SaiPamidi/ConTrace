import random
import csv

data = list(csv.reader(open('../simulated-data/ClassInfo.csv')))[1:]
print(data)
roomInfo = list(csv.reader(open('../simulated-data/RoomInfo.csv')))[1:]
roomCapacity = {}
for i in range(len(roomInfo)):
    roomCapacity[roomInfo[i][0]] = roomInfo[i][6]
studentList = [i for i in range(5001)]
studentTimeSchedule = {}
studentClassList = {}
for i in studentList:
    studentTimeSchedule[i] = {'m': [0]*9, 't': [0]
                              * 9, 'w': [0]*9, 'r': [0]*9, 'f': [0]*9}
for i in studentList:
    studentClassList[i] = {}
conversionTime = {'8:10': 0, '9:10': 1, '10:10': 2, '11:10': 3,
                  '12:10': 4, '1:10': 5, '2:10': 6, '3:10': 7, '4:10': 8, '5:10': 9}
scheduleInfo = [['StudentId', 'CourseId', 'Section no', 'seat no']]
days = ['m', 't', 'w', 'r', 'f']
for i in range(0, len(data)):
    data[i][7] = int(data[i][7])
#ClassInfo(CourseId, SectionNo, FacultyId, startTime, endTime, RoomID, M, T, W,Thu, F, StudentCapacity)


def getDays(num):
    gate = 1
    arr = []
    for i in days[::-1]:
        res = num & gate
        if res == 1:
            arr.append(i)
        num >> 1
    return arr


for i in studentList:
    z = random.randint(1, 10)
    if 1 <= z <= 8:
        classNum = 3
    else:
        classNum = 4

    for n in range(classNum):
        c1 = True
        c2 = True
        c3 = True
        while(c1 or c2 or c3):
            # print(i)
            c1 = False
            c2 = False
            c3 = False
            indx = random.randint(0, len(data)-1)
            classInfo = data[indx]
            # print(classInfo)
            classTime = conversionTime[classInfo[3]]
            classDuration = conversionTime[classInfo[4]
                                           ] - conversionTime[classInfo[3]]
            # print(classDuration)
            if classInfo[0] in studentClassList[i]:
                c3 = True
            for d in getDays(int(classInfo[6])):
                #print(studentTimeSchedule[i][days[d - 6]][classTime])
                if studentTimeSchedule[i][d][classTime] != 0:
                    c1 = True
                    break
                if classDuration == 2 and studentTimeSchedule[i][d][classTime + 1] != 0:
                    c2 = True
                    break
        studentClassList[i][classInfo[0]] = 1
        for d in getDays(int(classInfo[6])):
            studentTimeSchedule[i][d][classTime] += 1
            if classDuration == 2:
                studentTimeSchedule[i][d][classTime + 1] += 1
        # ScheduleInfo(StudentId, CourseId, Section no, seat no)
        scheduleInfo.append(
            [i, classInfo[0], classInfo[1], int(roomCapacity[classInfo[5]]) - data[indx][7] + 1])

        data[indx][7] -= 1
        if data[indx][7] == 0:
            print('here')
            del data[indx]
# print(scheduleInfo)
# print(studentTimeSchedule)
for s in studentTimeSchedule:
    for d in studentTimeSchedule[s]:
        for i in studentTimeSchedule[s][d]:
            if i > 1:
                print(True)
with open('../simulated-data/ScheduleInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(scheduleInfo)

for i in data:
    print('c', data[indx])
