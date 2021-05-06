import sqlite3 as sql
from sqlite3 import Error
import datetime
import time
from contactTracingAlgorithm import *

# seperate susceptible, exposed and infected sets

INFECTED = 1
EXPOSED = 0

conversionTime1 = {0: '8:10', 1: '9:10', 2: '10:10', 3: '11:10',
                   4: '12:10', 5: '1:10', 6: '2:10', 7: '3:10', 8: '4:10', 9: '5:10'}
conversionTime2 = {'8:10': 0, '9:10': 1, '10:10': 2, '11:10': 3,
                   '12:10': 4, '1:10': 5, '2:10': 6, '3:10': 7, '4:10': 8, '5:10': 9}


class Node:
    def __init__(self, sid, state, time_of_infection, prob_of_infection):
        self.sid = sid
        self.state = state
        self.time_of_infection = time_of_infection
        self.prob_of_infection = prob_of_infection


InfectedList = [{'ID': 4, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 21, 'time': '8:00'}}, {
    'ID': 2, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 22, 'time': '8:00'}}, {'ID': 3, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 23, 'time': '8:00'}}]


# made changes so that this function returns a list of studentID's that are infected
def check_exposed_is_infectious(student_nodes, cur_date, cur_time, incubationPeriod, 
    infected_students, exposed_students):
    to_remove = set()

    for student_id in exposed_students:
        cur_node = student_nodes[student_id]
        date_of_infection = datetime.date(
            cur_node.time_of_infection['year'], cur_node.time_of_infection['month'], cur_node.time_of_infection['day'])
        time_of_infection = cur_node.time_of_infection['time']
        if (date_of_infection + datetime.timedelta(incubationPeriod) <= cur_date) and conversionTime2[time_of_infection] <= conversionTime2[cur_time]:
            student_nodes[student_id].state = INFECTED
            new_date_of_infection = date_of_infection + \
                datetime.timedelta(incubationPeriod)
            student_nodes[student_id].time_of_infection = {
                'year': new_date_of_infection.year, 'month': new_date_of_infection.month, 'day': new_date_of_infection.day, 'time': time_of_infection}
            infected_students.add(cur_node.sid)
            to_remove.add(cur_node.sid)

    exposed_students -= to_remove


def getDays(num):
    gate = 1
    arr = []
    for _ in range(5):
        res = num & gate
        arr.append(res)
        num >> 1
    return arr[::-1]

# query -> get course and section based on student id , day and time
def get_course_from_time(student_id, day, time, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT ClassInfo.CourseID, ClassInfo.SectionNo, ClassInfo.Days 
                    FROM ClassInfo
                    INNER JOIN ScheduleInfo on ScheduleInfo.CourseID = ClassInfo.CourseID AND ScheduleInfo.SectionNo = ClassInfo.SectionNo 
                    WHERE ClassInfo.StartTime = ? AND ScheduleInfo.StudentID = ?''',
        (time, student_id,))

    courses = cur.fetchall()

    # week_num is passed through as day
    day_mask = 1 << day

    for course in courses:
        if course[-1] & day:
            return course[:-1]

    return []

def get_neighbors_in_course(student_id, course_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT NeighborID, Distance, Duration
                    FROM ContactGraph
                    WHERE StudentID = ? AND CourseID = ? ''', (student_id, course_id,))
    return cur.fetchall()

def get_student_classes(student_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT CourseID, SectionNo
                    FROM ScheduleInfo
                    WHERE StudentID = ? ''', (student_id,))

    return cur.fetchall()

def is_class_today(course_id, section_no, cur_time, week_num, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT Days
                    FROM ClassInfo
                    WHERE CourseID = ? AND SectionNo = ? AND StartTime = ? ''',
                    (course_id, section_no, cur_time,))

    class_days = cur.fetchone()

    day_mask = 1 << (4 - week_num)

    print(bin(class_days[0]))
    print(bin(day_mask))
    print(bin(class_days[0] & day_mask))

    return class_days != None and (class_days[0] & day_mask)

def get_infected_neighbors(student_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT NeighborId,CourseId,SectionNo,Distance,Duration FROM ContactGraph WHERE StudentId = ? ''',
                (student_id,))
    return cur.fetchall()
    

def forward_trace(student_nodes, cur_date, cur_time, incubationPeriod, infected_students,
    exposed_students, conn):
    check_exposed_is_infectious(
        student_nodes, cur_date, cur_time, incubationPeriod, infected_students, exposed_students)
    week_num = cur_date.weekday()

    for student_id in infected_students:
        cur_node = student_nodes[student_id]

        courses = get_student_classes(student_id, conn)
        selected_course = None

        for c in courses:
            cid = c[0]
            sno = c[1]
            if is_class_today(cid, sno, cur_time, week_num, conn):
                selected_course = cid
                break

        if selected_course == None:
            continue

        neighbors = get_neighbors_in_course(student_id, selected_course, conn)
        # print(len(neighbors))

        for n in neighbors:
            neighbor_id = n[0]
            distance = n[1]
            duration = n[2]
            prob_transmission = CalculateProb(distance, duration)
            prob_infection = student_nodes[student_id].prob_of_infection * \
                prob_transmission

            # neighbor is either susceptible or exposed to a greater risk
            if neighbor_id not in student_nodes or student_nodes[neighbor_id].prob_of_infection < prob_infection:
                exposed_students.add(neighbor_id)
                student_nodes[neighbor_id] = Node(neighbor_id, EXPOSED, {'year': cur_date.year, 
                    'month': cur_date.month, 'day': cur_date.day, 'time': cur_time}, prob_infection)


def IndirectContactTracing(InfectedList, incubationPeriod, conn):

    num_students = 5000
    student_nodes = {}
    infected_students = set()
    exposed_students = set()

    # sort Infected List - maybe

    earliest_infection = InfectedList[0]['TimeOfInfection']
    earliest_infection_date = datetime.date(
        earliest_infection['year'], earliest_infection['month'], earliest_infection['day'])

    for student in InfectedList:
        infected_students.add(student['ID'])
        student_nodes[student['ID']] = Node(student['ID'], INFECTED, student['TimeOfInfection'], 1.0)

    present_date = datetime.date.today()
    cur_date = earliest_infection_date

    while(cur_date != present_date):
        # print('here')
        print('E', len(
            [student_nodes[n].state for n in student_nodes if student_nodes[n].state == EXPOSED]))
        print('S', len(
            [student_nodes[n].state for n in student_nodes if student_nodes[n].state == INFECTED]))
        week_num = cur_date.weekday()

        if week_num in [5, 6]:
            cur_date = cur_date + datetime.timedelta(1)
            continue

        for i in range(9):
            cur_time = conversionTime1[i]
            forward_trace(student_nodes, cur_date,
                        cur_time, incubationPeriod, infected_students, 
                        exposed_students, conn)
        cur_date = cur_date + datetime.timedelta(1)

    print(len([(student_nodes[n].sid, student_nodes[n].prob_of_infection)
           for n in student_nodes if student_nodes[n].prob_of_infection > .15]))
                


""" def forward_trace(student_nodes, cur_date, cur_time, incubationPeriod, conn):
    check_exposed_is_infectious(
        student_nodes, cur_date, cur_time, incubationPeriod)
    week_num = cur_date.weekday()
    for student_id in student_nodes:
        cur_node = student_nodes[student_id]
        if cur_node.state == 'infected':
            neighbors = get_infected_neighbors(
                student_id, conn)
            # print(len(neighbors))
            for n in neighbors:
                neighbor_id = n[0]
                course_id = n[1]
                section_no = n[2]
                distance = n[3]
                duration = n[4]
                class_info = get_class_info(course_id, section_no, conn)
                start_time = class_info[0]
                days = class_info[1]
                neighbor_state = student_nodes[neighbor_id].state
                if (conversionTime2[start_time] == conversionTime2[cur_time]) and getDays(days)[week_num] == 1 \
                        and neighbor_state != 'infected':
                    # student_nodes[neighbor_id].prob_of_infection = (student_nodes[neighbor_id].state == 'susceptible') ? (true): (false)
                    prob_transmission = CalculateProb(distance, duration)
                    prob_infection = student_nodes[student_id].prob_of_infection * \
                        prob_transmission
                    if neighbor_state == 'susceptible' or student_nodes[neighbor_id].prob_of_infection < prob_infection:
                        student_nodes[neighbor_id].state = 'exposed'
                        year = cur_date.year
                        month = cur_date.month
                        day = cur_date.day
                        student_nodes[neighbor_id].time_of_infection['year'] = year
                        student_nodes[neighbor_id].time_of_infection['month'] = month
                        student_nodes[neighbor_id].time_of_infection['day'] = day
                        student_nodes[neighbor_id].time_of_infection['time'] = cur_time
                        student_nodes[neighbor_id].prob_of_infection = prob_infection """


'''def IndirectContactTracing(InfectedList, incubationPeriod, conn):

    num_students = 5000
    student_nodes = {}
    for student_id in range(0, num_students):
        student_nodes[student_id] = Node(
            student_id, 'susceptible', {'year': 0, 'month': 0, 'day': 0, 'time': ''}, 0)

    # sort Infected List - maybe

    earliest_infection = InfectedList[0]['TimeOfInfection']
    earliest_infection_date = datetime.date(
        earliest_infection['year'], earliest_infection['month'], earliest_infection['day'])

    for student in InfectedList:
        student_nodes[student['ID']].state = 'infected'
        student_nodes[student['ID']
                      ].time_of_infection = student['TimeOfInfection']
        student_nodes[student['ID']].prob_of_infection = 1

    present_date = datetime.date.today()
    cur_date = earliest_infection_date

    while(cur_date != present_date):
        # print('here')
        print('E', len(
            [student_nodes[n].state for n in student_nodes if student_nodes[n].state == 'exposed']))
        print('S', len(
            [student_nodes[n].state for n in student_nodes if student_nodes[n].state == 'infected']))
        week_num = cur_date.weekday()

        if week_num in [5, 6]:
            print("weekend\n")
            cur_date = cur_date + datetime.timedelta(1)
            continue

        for i in range(9):
            cur_time = conversionTime1[i]
            forward_trace(student_nodes, cur_date,
                          cur_time, incubationPeriod, conn)
        cur_date = cur_date + datetime.timedelta(1)

    print(len([(student_nodes[n].sid, student_nodes[n].prob_of_infection)
           for n in student_nodes if student_nodes[n].prob_of_infection > .50]))'''


conn = create_connection('contact_data.db')

start = time.time()
print("Potentially Infected Individuals: ", end='')
IndirectContactTracing(InfectedList, 3, conn)
stop = time.time()
print("Execution Time: %d seconds" % (stop - start))
