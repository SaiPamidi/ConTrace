import time
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_data():
	if request.method == 'POST':
		f = request.files['file']
		f.save()
		return "test"
	
flask_cors.CORS(app, expose_headers'Authorization')