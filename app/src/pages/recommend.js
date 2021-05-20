import React, { Component } from "react";
import { MDBDataTable } from 'mdbreact';
import * as mdb from 'mdb-ui-kit';
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import ButtonAppBar from './buttonAppBar.js';
import Button from '@material-ui/core/Button';

class Recommend extends Component {
  constructor() {
    super();
    this.state = {
      list: []
    };
  }

  GenRecList = () => {
    console.log("Generating the rec list");
    fetch("/rec_list", {
      method: "GET",
    }).then(
      response => response.json()
    ).then(data => this.DatatablePage(data.row_data));


  }

  DatatablePage = (row_data) => {
    //console.log(row_data)
    var new_rows = []
    for (var i in row_data) {
      new_rows.push(row_data[i])
    }
    console.log(new_rows)


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
      rows: new_rows
    };
    return <center><MDBDataTable
      scrollY
      maxHeight="300px"
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
        {this.DatatablePage()}
        <center><Button onClick={() => this.GenRecList()} variant="contained" color="primary">
          Run
				</Button></center>
      </div>

    );
  }
}


export default Recommend;
