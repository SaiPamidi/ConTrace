import React, { Component } from "react";
import { MDBDataTable } from 'mdbreact';
import * as mdb from 'mdb-ui-kit';
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import { BrowserRouter, Route, Switch, Link } from 'react-router-dom'
import ButtonAppBar from './buttonAppBar.js';
import Button from '@material-ui/core/Button';
import { CSVLink, CSVDownload } from "react-csv";

class Recommend extends Component {
  constructor() {
    super();
    this.state = {
      list: [],
      rows: [],
      download_data: []
    };
  }

  GenRecList = () => {
    console.log("Generating the rec list");
    fetch("/rec_list", {
      method: "GET",
    }).then(
      response => response.json()
    ).then(data => this.updateTable(data.row_data));


  }


  updateTable = (row_data) => {
    var new_rows = []
    var new_csv_data = [['Student_id', 'risk', 'age', 'degree', 'prob']]
    for (var i in row_data) {
      new_rows.push(row_data[i])
      new_csv_data.push([row_data[i].student_id, row_data[i].risk, row_data[i].age, row_data[i].degree, row_data[i].prob])
    }
    console.log(new_rows)
    this.setState({ rows: new_rows })
    this.setState({ download_data: new_csv_data })
  }

  DatatablePage = (row_data) => {
    //console.log(row_data)
    /*var new_rows = []
    for (var i in row_data) {
      new_rows.push(row_data[i])
    }
    console.log(new_rows)*/
    console.log(this.state.rows)

    var data = {
      columns: [
        {
          label: 'Student ID',
          field: 'student_id',
          sort: 'asc',
          width: 100
        },
        {
          label: 'Risk Level',
          field: 'risk',
          sort: 'asc',
          width: 100
        },
        {
          label: 'Prob of Infection',
          field: 'prob',
          sort: 'asc',
          width: 100
        },
        {
          label: 'Degree',
          field: 'degree',
          sort: 'asc',
          width: 100
        },
        {
          label: 'Age',
          field: 'age',
          sort: 'asc',
          width: 100
        }
      ],
      rows: this.state.rows
    };
    return <center><MDBDataTable
      scrollY
      maxHeight="500px"
      striped
      bordered
      small
      data={data}
    /></center>
  }

  render() {
    return (
      <div>
        <ButtonAppBar heading={`Recommended Actions`} />
        {this.DatatablePage(this.state.rows)}
        <center><Button onClick={() => this.GenRecList()} variant="contained" color="primary">
          Run
				</Button>
        </center>
        <CSVLink data={this.state.download_data}>Download REC list</CSVLink>
      </div>

    );
  }
}


export default Recommend;
