import sqlite3 as sql
from sqlite3 import Error


def make_title(student_id, student_nodes, conn):
    firstName, lastName, Age = get_name_age(student_id, conn)

    prob_of_infection = 0
    if student_id in student_nodes:
        prob_of_infection = student_nodes[student_id].prob_of_infection

    title = "ID : " + str(student_id) + "\n" + \
            "Name : " + firstName + ' ' + lastName + "\n" + \
            "Prob of Infection : " + str(prob_of_infection * 100) + "%\n" + \
            "Age : " + str(Age) + "\n"

    return title


def get_neighbors_ssv(student_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT DISTINCT NeighborID,Distance
                    FROM ContactGraph 
                    WHERE StudentID = ?''', (student_id,))

    return cur.fetchall()


def get_name_age(student_id, conn):
    cur = conn.cursor()
    cur.execute(
        ''' SELECT FirstName,LastName,Age FROM StudentInfo WHERE StudentId = ?''', (student_id,))
    return cur.fetchone()


#print(get_name_age(1, create_connection('contact_data.db')))
