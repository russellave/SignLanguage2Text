import React, { Component } from "react"
import './vid2text_input.css';
import axios from 'axios';

class Vid2TextInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selected_file: null,
            display_str: ''
        }
    }

    updateFile = event => {
        console.log(event.target.files[0]);
        this.setState({
            selected_file: event.target.files[0]
        })

    }

    getTranslation = () => {
        console.log("In getTranslation")
        console.log(this.state)
        const data = new FormData()
        data.append('video', this.state.selected_file)
        console.log(data.entries())
        axios.post("http://localhost:5000/vid2text", data).then(res => {
            console.log(res);
            this.setState({
                display_str: res.data,
                responseStatusOK: (res.status === 200)
            })
        })
    }


    render() {
        return (

            <div>
                <input type="file" className="form-control" multiple="" onChange={this.updateFile} />
                <button type="button" className="btn btn-success btn-block" onClick={this.getTranslation}>Get Word Level Translation</button>

                {
                    this.state.display_str !== '' ? 
                    <h1> {this.state.display_str} </h1>
                    :
                    <h1> didn't translate yet :( </h1>
                } 
            </div>
        )
    }
}

export default Vid2TextInput;