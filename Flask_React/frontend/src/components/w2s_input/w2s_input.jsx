import React, { Component } from "react"
import './w2s_input.css';
import axios from 'axios';

class W2SInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            input_text: '',
            display_str: ''
        }
    }

    updateText = (event) => {
        // console.log(event.target.value);
        this.setState({
            input_text: event.target.value
        })
    }

    generate = () => {
        const data = new FormData();
        data.append('input', this.state.input_text)
        console.log(data)
        axios.post("http://localhost:5000/w2s", data).then(res => {
            console.log(res);
            this.setState({
                display_str: res.data
            })
        }
        )

    }

    render() {
        return (

            <div>
                <input type="text" placeholder ="Input text" onChange={this.updateText}/>
                <button type="button" className="btn btn-primary" onClick={this.generate}>Get Sentence</button>
                {
                    this.state.display_str !== '' ? 
                    <h1> {this.state.display_str} </h1>
                    :
                    <h1> didn't get sentence yet :( </h1>
                } 
            </div>
        )
    }
}

export default W2SInput;