import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { DropzoneArea } from 'material-ui-dropzone';
import 'fontsource-roboto';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import ButtonAppBar from './buttonAppBar.js';
import axios from "axios";

import '../App.css';

class Home extends Component{
	constructor(props) {
		super(props);
		this.state = {
			files: []
		};
	}
	handleChange(files) {
		this.setState({
			files: files
		});
	}
	
	state = {
		text: "Upload"
	}
	
	changeText = (text) => {
		this.setState({ text });
	}
	
	fileUploader = (files) => {
		console.log("Trying to call api");
		const formData = new FormData();

		const file = files[0];
		formData.append(file.name, file);

		fetch("/analyze", {
			method: "POST",
			body: formData,
		}).then(response => response.json().then(console.log(response.text)));
	}
	
	render() {
		const { text } = this.state
		return(
		<div className = "Home">
			<div>
			<ButtonAppBar heading={`Upload`}/>
			</div>
		  <h1><center>Submit Files</center></h1>
		  	<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload StudentInfo(StudentId,LastName,FirstName)"
			showAlerts={false}
			filesLimit={1}
			onDrop={this.fileUploader}/>
			<br/>
			<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload FacultyInfo(FacultyId,LastName,FirstName)"
			showAlerts={false}
			filesLimit={1}/>
			<br/>
			<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload CourseInfo(CourseId,CourseName)"
			showAlerts={false}
			filesLimit={1}/>
			<br/>
			<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload RoomInfo(RoomId,BuildingName,RoomNo,Length,Width,StudentCapacity)"
			showAlerts={false}
			filesLimit={1}/>
			<br/>
			<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload ClassInfo(CourseId,SectionNo,FacultyId,startTime,endTime,RoomId,m,t,w,r,f,StudentCapacity)"
			showAlerts={false}
			filesLimit={1}/>
			<br/>
			<DropzoneArea
			acceptedFiles={[".csv, text/csv, application/vnd.ms-excel, application/csv, text/x-csv, application/x-csv, text/comma-separated-values, text/x-comma-separated-values"]}
			onChange={this.handleChange.bind(this)}
			showFileNames
			dropzoneText="Upload ScheduleInfo(StudentId,CourseId,SectionNo,SeatNo)"
			showAlerts={false}
			filesLimit={1}/>
			<br/>
			<center><Button onClick={ () => { this.changeText("Loading...")} } variant="contained" color="primary">
				{text}
			</Button></center>
			</div>
		);
	}
}

export default Home;