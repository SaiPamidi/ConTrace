import time
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import os
import shutil
from populate_db import *

app = Flask(__name__)
app.config['UPLOAD_PATH'] = './resources'
CORS(app)

if not os.path.exists('./resources'):
	os.makedirs('./resources')
else:
	shutil.rmtree('./resources')
	os.makedirs('./resources')

@app.route('/student_info', methods=['GET', 'POST'])
def student_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/StudentInfo.csv')

		pop_table('test.db', './resources/StudentInfo.csv', create_student)
		print('Finished populating students')
		return "test"
		
@app.route('/faculty_info', methods=['GET', 'POST'])
def faculty_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/FacultyInfo.csv')
		pop_table('test.db', './resources/FacultyInfo.csv', create_faculty)
		return "test"

@app.route('/course_info', methods=['GET', 'POST'])
def course_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/CourseInfo.csv')
		pop_table('test.db', './resources/CourseInfo.csv', create_course)
		return "test"

@app.route('/room_info', methods=['GET', 'POST'])
def room_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/RoomInfo.csv')
		pop_table('test.db', './resources/RoomInfo.csv', create_room)
		return "test"

@app.route('/class_info', methods=['GET', 'POST'])
def class_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/ClassInfo.csv')
		pop_table('test.db', './resources/ClassInfo.csv', create_class)
		return "test"

@app.route('/schedule_info', methods=['GET', 'POST'])
def schedule_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/ScheduleInfo.csv')
		pop_table('test.db', './resources/ScheduleInfo.csv', create_schedule_entry)
		return "test"

@app.route('/infected_students', methods=['GET', 'POST'])
def infected_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/InfectedStudents.csv')
		return "test"

CORS(app, expose_headers = 'Authorization')