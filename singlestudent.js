import React, { Component } from "react";
import Graph from "react-graph-vis";
import ButtonAppBar from './buttonAppBar.js';
import SearchBar from "material-ui-search-bar";

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
				arrows:{
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
			  { id: 1, label: "Node 1" },
			  { id: 2, label: "Node 2" },
			  { id: 3, label: "Node 3" },
			  { id: 4, label: "Node 4" },
			  { id: 5, label: "Node 5" }
			],
			edges: [
			  { from: 1, to: 2 },
			  { from: 1, to: 3 },
			  { from: 2, to: 4 },
			  { from: 2, to: 5 }
			]
		}
		};
	}

	componentDidMount() {
		document.addEventListener("mousedown", e => {});
		document.addEventListener("mousemove", e => {});
	}

	events = {
		dragStart: event => {},
		dragEnd: event => {}
	};

	getGraph = () => {
		fetch("/get_neighbors", {
			method: "POST",
			body : JSON.stringify(this.state.data),
		}).then(
			response => response.json()
		  ).then(data => console.log(data));
	}

	render() {
	return (
	
		<div id="graph" style={{ height: "100vh" }}>
			<div>
				<ButtonAppBar heading={`Single Student`}/>
				<SearchBar
					placeholder="Input Student ID..."
					value={this.state.data}
					onChange={(newData) => this.setState({data : newData}) }
					onRequestSearch={this.getGraph()}
					onCancelSearch={() => console.log('cancelled search')}
					autoFocus
				/>
			</div>
			<Graph
				graph={this.state.graph}
				options={this.state.options}
				events={this.state.events}
			/>
		</div>
		);
	}
}

export default SingleStudent;