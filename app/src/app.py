from IndirectContactTracing import *
from build_contact_graph import *
from RecTestingList import*
from populate_db import *
from support import *
import shutil
import time
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import os
import json
import csv

app = Flask(__name__)
app.config['UPLOAD_PATH'] = './resources'
CORS(app)

# if os.path.exists('./resources'):
#	shutil.rmtree('./resources')
# os.makedirs('./resources')

# if os.path.exists('./contact_data.db'):
#	os.remove('./contact_data.db')
# create_db()

student_nodes = {}


@app.route('/student_info', methods=['GET', 'POST'])
def student_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/StudentInfo.csv'
        # f.save(path)

        #pop_table('contact_data.db', path, create_student)
        print('Finished populating students')
        return "student_upload test"


@app.route('/faculty_info', methods=['GET', 'POST'])
def faculty_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/FacultyInfo.csv'
        # f.save(path)
        #pop_table('contact_data.db', path, create_faculty)
        return "faculty_upload test"


@app.route('/course_info', methods=['GET', 'POST'])
def course_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/CourseInfo.csv'
        # f.save(path)
        #pop_table('contact_data.db', path, create_course)
        return "course_upload test"


@app.route('/room_info', methods=['GET', 'POST'])
def room_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/RoomInfo.csv'
        # f.save(path)
        #pop_table('contact_data.db', path, create_room)
        return "room_upload test"


@app.route('/class_info', methods=['GET', 'POST'])
def class_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/ClassInfo.csv'
        # f.save(path)
        #pop_table('contact_data.db', path, create_class)
        return "class_upload test"


@app.route('/schedule_info', methods=['GET', 'POST'])
def schedule_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/ScheduleInfo.csv'
        # f.save(path)
        #pop_table('contact_data.db', path, create_schedule_entry)
        return "schedule_upload test"


@app.route('/infected_students', methods=['GET', 'POST'])
def infected_upload():
    if request.method == 'POST':
        print("Saving file")
        f = request.files['file']
        path = app.config['UPLOAD_PATH'] + '/InfectedStudents.csv'
        # f.save(path)
        return "infected_upload test"


@app.route('/build_graph', methods=['GET', 'POST'])
def flask_build_graph():
    if request.method == 'GET':
        print("Building graph")
        conn = create_connection('./contact_data.db')
        # build_graph(conn)
        InfectedList = parse_infected(
            app.config['UPLOAD_PATH'] + '/InfectedStudents.csv')
        nodes = IndirectContactTracing(InfectedList, 3, conn)
        # print('here', nodes)
        for s in nodes:
            student_nodes[s] = nodes[s]
        return jsonify(student_nodes)


@app.route('/get_neighbors', methods=['POST'])
def flask_get_neighbors():
    if request.method == 'POST':
        print('getting ID')
        student_id = int(request.data)
        conn = create_connection('contact_data.db')
        neighbor_ids = get_neighbors_ssv(student_id, conn)
        title = make_title(student_id, student_nodes, conn)
        nodes = [{"id": student_id, "label": str(student_id), 'title': title}]
        edges = []
        for n in neighbor_ids:
            print(n[0])
            title = make_title(n[0], student_nodes, conn)
            nodes.append({"id": n[0], "label": str(n[0]),
                          "color": None, "title": title})
            edges.append({"from": student_id, "to": n[0], "length": n[1]})

        app_dict = {"nodes": nodes, "edges": edges}
        return json.dumps(app_dict)


@app.route('/get_student_nodes', methods=['GET'])
def flask_get_student_nodes():
    if request.method == 'GET':
        print(len(student_nodes))
        return jsonify(student_nodes)


@app.route('/rec_list', methods=['GET'])
def gen_list():
    if request.method == 'GET':
        print("sending_list")
        conn = create_connection('contact_data.db')
        testing_list = testing_rec_lists(student_nodes, conn)
        rows = []
        for s in testing_list:
            rows.append({
                'student_id': s.student_id,
                'risk': s.tier,
                'prob': s.prob_of_infection,
                'degree': s.degree,
                'age': s.age
            })

    return {'row_data': rows}


CORS(app, expose_headers='Authorization')
