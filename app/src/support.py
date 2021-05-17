import sqlite3 as sql
from sqlite3 import Error


def get_neighbors_ssv(student_id, conn):
    cur = conn.cursor()
    cur.execute(''' SELECT DISTINCT NeighborID
                    FROM ContactGraph 
                    WHERE StudentID = ?''', (student_id,))

    return cur.fetchall()
