import time
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import os
import shutil

app = Flask(__name__)
app.config['UPLOAD_PATH'] = './resources'
CORS(app)

if not os.path.exists('./resources'):
	os.makedirs('./resources')
else:
	shutil.rmtree('./resources')

@app.route('/student_info', methods=['GET', 'POST'])
def student_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/StudentInfo.csv')
		return "test"
		
@app.route('/faculty_info', methods=['GET', 'POST'])
def faculty_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/FacultyInfo.csv')
		return "test"

@app.route('/course_info', methods=['GET', 'POST'])
def course_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/CourseInfo.csv')
		return "test"

@app.route('/room_info', methods=['GET', 'POST'])
def room_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/RoomInfo.csv')
		return "test"

@app.route('/class_info', methods=['GET', 'POST'])
def class_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/ClassInfo.csv')
		return "test"

@app.route('/schedule_info', methods=['GET', 'POST'])
def schedule_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/ScheduleInfo.csv')
		return "test"

@app.route('/infected_students', methods=['GET', 'POST'])
def infected_upload():
	if request.method == 'POST':
		print("Saving file")
		f = request.files['file']
		f.save(app.config['UPLOAD_PATH'] + '/InfectedStudents.csv')
		return "test"

CORS(app, expose_headers = 'Authorization')