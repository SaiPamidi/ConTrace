import sqlite3 as sql
from sqlite3 import Error

InfectedList = [{'ID': 4, 'TimeOfInfrection': 1618786167.3532438}, {
    'ID': 2, 'TimeOfInfrection': 1618786167.3532438}, {'ID': 3, 'TimeOfInfrection': 1618786167.3532438}]

StudentsProbOfInfection = {}
for student_id in range(0, 5000):
    StudentsProbOfInfection[student_id] = 0


def create_connection(db_name):
    conn = None
    try:
        conn = sql.connect(db_name)
        return conn
    except Error as e:
        print(e)


def get_classes(student_id, conn):
    cur = conn.cursor()
    cur.execute(
        ''' SELECT CourseId,SectionNo FROM ScheduleInfo WHERE StudentID = ?''', (student_id,))
    classes = cur.fetchall()

    return classes


def get_infected_neighbors(student_id, course_id, section_no, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT NeighborId,ProbTrans FROM ContactGraph WHERE StudentId = ? AND ClassId = ? AND SectionNo = ? ''',
                (student_id, course_id, section_no))
    return cur.fetchall()


def DirectContactTracing(InfectedList, conn):
    for student in InfectedList:
        StudentsProbOfInfection[student['ID']] = 100
        classes = get_classes(student['ID'], conn)
        for c in classes:
            course_id = c[0]
            section_no = c[1]
            infected_neighbors = get_infected_neighbors(
                student['ID'], course_id, section_no, conn)
            for n in infected_neighbors:
                StudentsProbOfInfection[n[0]] = max(
                    StudentsProbOfInfection[n[0]], n[1])
    # print(StudentsProbOfInfection)
    # print([i for i in StudentsProbOfInfection if StudentsProbOfInfection[i] == 100])


DirectContactTracing(InfectedList, create_connection('contact_data.db'))
