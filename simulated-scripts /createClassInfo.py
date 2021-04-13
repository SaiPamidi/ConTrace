import random
import csv

facultyNum = 150
roomNum = 30
facultyTimeSchedule = {}
roomInfo = list(csv.reader(open('../simulated-data/RoomInfo.csv')))[1:]
roomCapacity = {}
for i in range(len(roomInfo)):
    roomCapacity[int(roomInfo[i][0])] = roomInfo[i][6]
roomTimeSchedule = {}
for i in range(0, facultyNum):
    facultyTimeSchedule[i] = {'m': [0]*9, 't': [0]
                              * 9, 'w': [0]*9, 'r': [0]*9, 'f': [0]*9}
courseList = [i for i in range(1, 151)]

for i in range(0, roomNum):
    roomTimeSchedule[i] = {'m': [0]*9, 't': [0]
                           * 9, 'w': [0]*9, 'r': [0]*9, 'f': [0]*9}

classOptions = [[['m', 'w', 'f'], 1], [
    ['t', 'r'], 2], [['m', 'w'], 2], [['w', 'f'], 2]]

conversionTime = {0: '8:10', 1: '9:10', 2: '10:10', 3: '11:10',
                  4: '12:10', 5: '1:10', 6: '2:10', 7: '3:10', 8: '4:10', 9: '5:10'}


classInfo = []
# data = [['CourseId', 'SectionNo', 'FacultyId', 'startTime', 'endTime',
#         'RoomID', 'm', 't', 'w', 'r', 'f', 'StudentCapacity']]
data = [['CourseId', 'SectionNo', 'FacultyId', 'startTime', 'endTime',
         'RoomID', 'Days', 'StudentCapacity']]


def getDays(arr):
    days = ['m', 't', 'w', 'r', 'f']
    res = 0
    # res = []
    # for i in days:
    #     if i in arr:
    #         res.append(1)
    #     else:
    #         res.append(0)
    for i in days:
        if i in arr:
            res = (res << 1) + 1
        else:
            res = res << 1
    return res


for i in range(0, facultyNum):
    # pick a course and del
    course = random.choice(courseList)
    courseList.remove(course)
    for s in range(1, 3):
        # ClassInfo(CourseId, SectionNo, FacultyId, startTime, endTime, RoomID, M, T, W,Thu, F, StudentCapacity)
        c1 = True
        c2 = True
        c3 = True
        while(c1 or c2 or c3):
            #print('here', i)
            c1 = False
            c2 = False
            c3 = False
            # chooses class structure
            classOption = random.choice(classOptions)
            # chooses class timming
            classTime = random.choice([i for i in range(9)])
            room = random.choice([i for i in range(roomNum)]
                                 )        # chooses a room
            if classOption[1] == 1:
                for d in classOption[0]:
                    if facultyTimeSchedule[i][d][classTime] != 0 or roomTimeSchedule[room][d][classTime] != 0:
                        c1 = True
                        break
            else:
                if classTime != 8:
                    for d in classOption[0]:
                        if facultyTimeSchedule[i][d][classTime] != 0 or roomTimeSchedule[room][d][classTime] != 0:
                            c2 = True
                            break
                        if facultyTimeSchedule[i][d][classTime + 1] != 0 or roomTimeSchedule[room][d][classTime + 1] != 0:
                            c3 = True
                            break
                else:
                    c1 = True

        for d in classOption[0]:
            facultyTimeSchedule[i][d][classTime] += 1
            roomTimeSchedule[room][d][classTime] += 1
            if classOption[1] == 2:
                facultyTimeSchedule[i][d][classTime + 1] += 1
                roomTimeSchedule[room][d][classTime + 1] += 1
        classInfo.append([course, 1, i, room, classTime,
                          classOption[1]] + [d for d in classOption[0]])

        # print(conversionTime[classTime + classOption[1]])
        data.append([course, s, i, conversionTime[classTime], conversionTime[classTime + classOption[1]], room] +
                    [getDays(classOption[0])] + [roomCapacity[room]])

# ClassInfo(CourseId, SectionNo, FacultyId, startTime, endTime, RoomID, M, T, W,Thu, F, StudentCapacity)

# print(roomTimeSchedule)
# print(facultyTimeSchedule)
for f in facultyTimeSchedule:
    for d in facultyTimeSchedule[f]:
        for i in facultyTimeSchedule[f][d]:
            if i > 1:
                print(True)
with open('simulated-data/ClassInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
