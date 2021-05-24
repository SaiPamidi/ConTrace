import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { DropzoneArea } from 'material-ui-dropzone';
import 'fontsource-roboto';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { Route, Redirect, Switch, BrowserRouter as Router, Link } from 'react-router-dom';

import '../App.css';

class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			files: [],
			text: "Run ConTrace",
			student_prob: {},
			upload_status: [0, 0, 0, 0, 0, 0, 0],
		};
	}
	handleChange(files) {
		this.setState({
			files: files
		});
	}

	changeText = (text) => {
		this.setState({ text: text });
	}

	fileUploader1 = async (files) => {
		const formData = new FormData();

		const file = await files[0];
		formData.append("file", file);

		const response = await fetch("/student_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[0] = 1
		this.setState({ upload_status: newstatus })
	}

	fileUploader2 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const respnse = await fetch("/faculty_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[1] = 1
		this.setState({ upload_status: newstatus })
	}

	fileUploader3 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const response = await fetch("/course_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[2] = 1
		this.setState({ upload_status: newstatus })
	}

	fileUploader4 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const response = await fetch("/room_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[3] = 1
		this.setState({ upload_status: newstatus })
	}

	fileUploader5 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const response = await fetch("/class_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[4] = 1
		this.setState({ upload_status: newstatus })
	}

	fileUploader6 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const response = await fetch("/schedule_info", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[5] = 1
		this.setState({ upload_status: newstatus })
	}
	fileUploader7 = async (files) => {
		const formData = new FormData();

		const file = files[0];
		formData.append("file", file);

		const response = await fetch("/infected_students", {
			method: "POST",
			body: formData,
		});

		var newstatus = this.state.upload_status
		newstatus[6] = 1
		this.setState({ upload_status: newstatus })
	}
	setStudentProb = (data) => {
		console.log(data)
		this.setState({ student_prob: data })

	}

	buildGraph = async () => {
		console.log("Building graph")
		this.changeText("Loading...")
		const response = await fetch("/build_graph", {
			method: "GET",
		}).then(response => response.json().then(data => { this.setStudentProb(data) }));
		this.changeText("Done")

		window.location.href = "/singlestudent"
	}

	asynchHandler = () => {
		this.buildGraph(this.changeText);
	}

	render() {
		const { text } = this.state
		let ready = 1;
		let button;
		//console.log(this.state.upload_status)
		/*for (var i in this.state.upload_status) {
			if (this.state.upload_status[i] == 0) {
				ready = 0;
				break;
			}
		}*/

		if (ready == 1) {
			button = <Button onClick={this.buildGraph} variant="contained" color="primary">{text}</Button>
		}
		else {
			button = <Button onClick={() => alert('Uploading not complete')} variant="contained" color="primary">{text}</Button>
		}
		return (
			<div className="Home">
				<h1><center>Submit Files</center></h1>
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload StudentInfo(StudentId,LastName,FirstName,Age)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader1} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload FacultyInfo(FacultyId,LastName,FirstName,Age)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader2} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload CourseInfo(CourseId,CourseName)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader3} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload RoomInfo(RoomId,BuildingName,RoomNo,Length,Width,StudentCapacity)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader4} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload ClassInfo(CourseId,SectionNo,FacultyId,startTime,endTime,RoomId,m,t,w,r,f,StudentCapacity)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader5} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload ScheduleInfo(StudentId,CourseId,SectionNo,SeatNo)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader6} />
				<br />
				<DropzoneArea
					acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
					onChange={this.handleChange.bind(this)}
					showFileNames
					dropzoneText="Upload InfectedStudents(StudentId,Year,Day,Month,Time)"
					showAlerts={false}
					filesLimit={1}
					onDrop={this.fileUploader7} />
				<br />
				<center>{button}</center>
			</div>
		);
	}
}

export default Home;