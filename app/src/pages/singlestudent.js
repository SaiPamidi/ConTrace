import React, { Component } from "react";
import Graph from "react-graph-vis";
import ButtonAppBar from './buttonAppBar.js';
import SearchBar from "material-ui-search-bar";
import Button from '@material-ui/core/Button';
import { v4 as uuidv4 } from 'uuid';

class SingleStudent extends Component {
  constructor() {
    super();
    this.state = {
      data: "",
      options: {
        layout: {
          // hierarchical: true,
        },
        edges: {
          color: "#000000",
          arrows: {
            to: {
              enabled: false
            },
            from: {
              enabled: false
            }
          }
        },
        nodes: {
          color: "#888f99"
        },
        physics: {
          enabled: true
        },
        interaction: { multiselect: true, dragView: true }
      },
      graph: {
        nodes: [
        ],
        edges: [

        ]
      },
      network: null
    };
  }
  /*{ from: 1, to: 2 },
          { from: 1, to: 3, color: "#FF0000" },
          { from: 2, to: 4 },
          { from: 2, to: 5 }*/
  /*{ id: 1, label: "Node 1" },
            { id: 2, label: "Node 2" },
            { id: 3, label: "Node 3" },
            { id: 4, label: "Node 4" },
            { id: 5, label: "Node 5" }*/

  componentDidMount() {
    document.addEventListener("mousedown", e => { });
    document.addEventListener("mousemove", e => { });
  }

  events = {
    dragStart: event => { },
    dragEnd: event => { }
  };

  handleChange = (newData) => {
    //console.log(this.props.location.state[0].student_prob);
    this.setState({ data: newData })
  }

  setColor = (node) => {
    var student_prob = this.props.location.state[0].student_prob
    var infection_prob = student_prob[node.id]
    if (infection_prob < 0.35) {
      node.color = '#F88379'
    }
    else if (infection_prob < 0.70) {
      node.color = '#CD5C5C'
    }
    else {
      node.color = '#CF352E'
    }
  }

  parseNodes = (output) => {
    console.log(output);

    //this.state.graph.nodes = []
    //this.state.graph.edges = []

    var new_nodes = []
    var new_edges = []
    for (var node in output.nodes) {
      this.setColor(output.nodes[node]);
      console.log(output.nodes[node]);
      new_nodes.push(output.nodes[node]);
    }
    for (var node in output.edges) {
      output.edges[node].length = output.edges[node].length * 4;
      console.log(output.edges[node]);
      new_edges.push(output.edges[node]);
    }

    this.setState({
      graph: {
        nodes: new_nodes, edges: new_edges
      }
    });
    /*var nodesCopy = this.state.graph.nodes.slice(); // this will create a copy with the same items
    nodesCopy.push({ id: 7, label: '7' });
    this.state = { graph: { nodes: [], edges: [] } };
    this.setState({ graph: { nodes: nodesCopy, edges: [] } });*/
  }

  getGraph = (student_id) => {
    fetch("/get_neighbors", {
      method: "POST",
      body: student_id,
    }).then(
      response => response.json()
    ).then(data => this.parseNodes(data));
    //console.log(student_id);
    //this.setState({ nodes: response.json()['data'] })
  }

  render() {
    return (

      <div id="graph" style={{ height: "100vh" }}>
        <div>
          <ButtonAppBar heading={`Single Student`} />
          <SearchBar
            placeholder="Input Student ID..."
            onChange={this.handleChange}
            onRequestSearch={this.getGraph}
            onCancelSearch={() => console.log('cancelled search')}
            autoFocus
          />
        </div>
        <Graph
          key={uuidv4()}
          graph={this.state.graph}
          options={this.state.options}
          events={this.state.events}
        />
      </div>
    );
  }
}

export default SingleStudent;