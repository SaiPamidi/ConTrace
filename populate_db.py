import csv
import sqlite3 as sql
from sqlite3 import Error

def create_connection(db_name):
    conn = None
    try:
        conn = sql.connect(db_name)
        return conn
    except Error as e:
        print(e)

def create_student(conn, info):
    insert_info = """ INSERT INTO StudentInfo(StudentID, LastName, FirstName, Age)
					  VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid

def create_faculty(conn, info):
    insert_info = """ INSERT INTO FacultyInfo(FacultyID, LastName, FirstName, Age)
					  VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid

def create_course(conn, info):
    insert_info = """ INSERT INTO CourseInfo(CourseID, CourseName)
					  VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid

def create_room(conn, info):
    insert_info = """ INSERT INTO RoomInfo(RoomID, BuildingName, BuildingNo, RoomNo, Length, Width, StudentCapacity)
					  VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid

def create_class(conn, info):
    insert_info = """ INSERT INTO ClassInfo(CourseID, SectionNo, FacultyID, StartTime, EndTime, RoomID, Days, StudentCapacity)
					  VALUES(?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid

def create_schedule_entry(conn, info):
    insert_info = """ INSERT INTO ScheduleInfo(StudentID, CourseID, SectionNo, SeatNo)
					  VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(insert_info, info)
    conn.commit()
    return cur.lastrowid



def main():
	# first = True
	# conn = create_connection('contact_data.db')

	# with open('simulated-data/ClassInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_class(conn, row)

	# first = True
	# with open('simulated-data/CourseInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_course(conn, row)

	# first = True
	# with open('simulated-data/RoomInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_room(conn, row)

	# first = True
	# with open('simulated-data/FacultyInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_faculty(conn, row)

	# first = True
	# with open('simulated-data/StudentInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_student(conn, row)

	# first = True
	# with open('simulated-data/ScheduleInfo.csv') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		if first:
	# 			first = False
	# 		else:
	# 			create_schedule_entry(conn, row)

if __name__ == '__main__':
    main()
