# SIR Epidemics and Perlocation
import random
import csv
import sqlite3 as sql
from sqlite3 import Error
import math
import datetime
from contactTracingAlgorithm import *
from IndirectContactTracing import *


# building perlocated graph

def edge_outcome(prob_of_transmission):
    outcomes = [1, 0]
    outcome = random.choices(outcomes, weights=(
        prob_of_transmission, 1-prob_of_transmission))
    return outcome[0]


def add_edge(student_id, neighbor_id, course_id, section_no, conn):
    cur = conn.cursor()
    insert_info = """ INSERT INTO PerlocatedGraph(StudentID, NeighborID, CourseID, SectionNo)
					  VALUES(?,?,?,?) """
    cur.execute(insert_info, (student_id, neighbor_id, course_id, section_no))
    conn.commit()


def build_perlocated_graph(conn):
    cur = conn.cursor()
    cur.execute(''' SELECT * FROM ContactGraph''')
    while(True):
        row = cur.fetchone()
        if row == None:
            break
        student_id = row[0]
        neighbor_id = row[1]
        course_id = row[2]
        section_no = row[3]
        distance = row[4]
        duration = row[5]
        prob_of_transmission = CalculateProb(distance, duration)
        if edge_outcome(prob_of_transmission) == 1:
            add_edge(student_id, neighbor_id, course_id, section_no, conn)
    conn.close()


#conn = create_connection('contact_data.db')
# print(conn)
# build_perlocated_graph(conn)


# running SIR ALGORITHM

InfectedList = [{'ID': 4, 'TimeOfInfection': {'year': 2021, 'month': 4, 'day': 23, 'time': '8:00'}},
                {'ID': 98, 'TimeOfInfection': {'year': 2021,
                                               'month': 4, 'day': 24, 'time': '8:00'}},
                {'ID': 2001, 'TimeOfInfection': {'year': 2021,
                                                 'month': 4, 'day': 25, 'time': '8:00'}},
                {'ID': 2, 'TimeOfInfection': {'year': 2021,
                                              'month': 4, 'day': 26, 'time': '8:00'}}]


def check_exposed_is_infectious(student_nodes, cur_date, incubationPeriod, infected_students, exposed_students):
    to_remove = set()
    for student_id in exposed_students:
        cur_node = student_nodes[student_id]
        if cur_node.time_of_infection + datetime.timedelta(incubationPeriod) <= cur_date:
            student_nodes[student_id].state = INFECTED
            student_nodes[student_id].time_of_infection = cur_date
            infected_students.add(student_id)
            to_remove.add(student_id)
    exposed_students -= to_remove


def get_all_classes(student_id, conn):
    cur = conn.cursor()
    cur.execute(
        ''' SELECT CourseId,SectionNo FROM ScheduleInfo WHERE StudentId = ?''', (student_id,))
    return cur.fetchall()


def get_class_info(student_id, course_id, section_no, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT days FROM ClassInfo WHERE CourseId = ? AND SectionNo = ? ''',
                (course_id, section_no))
    return cur.fetchone()


def get_class_on_weeknum(student_id, week_num, conn):
    classes = get_all_classes(student_id, conn)
    filtered_classes = []
    for c in classes:
        course_id = c[0]
        section_no = c[1]
        days = get_class_info(student_id, course_id, section_no, conn)[0]
        day_mask = 1 << (4 - week_num)
        if days & day_mask:
            filtered_classes.append((course_id, section_no))
    return filtered_classes


def get_neighbors(student_id, course_id, section_no, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT NeighborID FROM ContactGraph WHERE StudentId = ? AND CourseID = ? AND SectionNo = ? ''',
                (student_id, course_id, section_no))
    return cur.fetchall()


def single_run(student_nodes, cur_date, incubationPeriod, infected_students, exposed_students, conn):
    check_exposed_is_infectious(
        student_nodes, cur_date, incubationPeriod, infected_students, exposed_students)

    week_num = cur_date.weekday()

    for student_id in infected_students:
        classes = get_class_on_weeknum(student_id, week_num, conn)
        for c in classes:
            course_id = c[0]
            section_no = c[1]
            neighbors = get_neighbors(student_id, course_id, section_no, conn)
            for n in neighbors:
                neighbor_id = n[0]
                student_nodes[neighbor_id].state = EXPOSED
                student_nodes[neighbor_id].time_of_infection = cur_date
                exposed_students.add(neighbor_id)


def run_SIR_model(InfectedList, incubationPeriod, conn):

    num_students = 5000
    student_nodes = {}
    for i in range(num_students):
        student_nodes[i] = Node(i, -1, 0, 0)

    infected_students = set()
    exposed_students = set()
    earliest_infected_student = InfectedList[0]
    earliest_infection_date = datetime.date(earliest_infected_student['TimeOfInfection']['year'],
                                            earliest_infected_student['TimeOfInfection']['month'],
                                            earliest_infected_student['TimeOfInfection']['day'])
    cur_date = earliest_infection_date
    present_date = datetime.date.today()

    while(cur_date != present_date):
        # print('here')
        week_num = cur_date.weekday()

        if week_num in [5, 6]:
            cur_date = cur_date + datetime.timedelta(1)
            continue

        InfectedList = update_infected(
            infected_students, InfectedList, cur_date)

        single_run(student_nodes, cur_date,
                   incubationPeriod, infected_students, exposed_students, conn)

        print('E', len(exposed_students))
        print('I', len(infected_students))

        cur_date = cur_date + datetime.timedelta(1)


conn = create_connection('contact_data.db')
run_SIR_model(InfectedList, 3, conn)
