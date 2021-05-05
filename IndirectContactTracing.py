import sqlite3 as sql
from sqlite3 import Error
import datetime
from contactTracingAlgorithm import *

# seperate susceptible, exposed and infected sets


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


InfectedList = [{'ID': 4, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 20, 'time': '8:00'}}, {
    'ID': 2, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 21, 'time': '8:00'}}, {'ID': 3, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 22, 'time': '8:00'}}]


def check_exposed_is_infectious(student_nodes, cur_date, cur_time, incubationPeriod):
    for student_id in student_nodes:
        cur_node = student_nodes[student_id]
        if cur_node.state == 'exposed':
            date_of_infection = datetime.date(
                cur_node.time_of_infection['year'], cur_node.time_of_infection['month'], cur_node.time_of_infection['day'])
            time_of_infection = cur_node.time_of_infection['time']
            if (date_of_infection + datetime.timedelta(incubationPeriod) <= cur_date) and conversionTime2[time_of_infection] <= conversionTime2[cur_time]:
                student_nodes[student_id].state = 'infected'
                new_date_of_infection = date_of_infection + \
                    datetime.timedelta(incubationPeriod)
                student_nodes[student_id].time_of_infection = {
                    'year': new_date_of_infection.year, 'month': new_date_of_infection.month, 'day': new_date_of_infection.day, 'time': time_of_infection}


def getDays(num):
    gate = 1
    arr = []
    for _ in range(5):
        res = num & gate
        arr.append(res)
        num >> 1
    return arr[::-1]

# query -> get course and section based on student id , day and time


def get_infected_neighbors(student_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT NeighborId,CourseId,SectionNo,Distance,Duration FROM ContactGraph WHERE StudentId = ? ''',
                (student_id,))
    return cur.fetchall()


def forward_trace(student_nodes, cur_date, cur_time, incubationPeriod, conn):
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
                        student_nodes[neighbor_id].prob_of_infection = prob_infection


def IndirectContactTracing(InfectedList, incubationPeriod, conn):

    num_students = 5000
    student_nodes = {}
    for student_id in range(0, num_students):
        student_nodes[student_id] = Node(
            student_id, 'sucpetible', {'year': 0, 'month': 0, 'day': 0, 'time': ''}, 0)

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

    print([(student_nodes[n].sid, student_nodes[n].prob_of_infection)
           for n in student_nodes if student_nodes[n].prob_of_infection > .50])


conn = create_connection('contact_data.db')

IndirectContactTracing(InfectedList, 3, conn)
