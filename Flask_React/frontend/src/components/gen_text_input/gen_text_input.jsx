import React, { Component } from "react"
import './gen_text_input.css';
import axios from 'axios';

class GenTextInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            input_text: '',
            display_str: '',
            genre: this.props.genre
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
        data.append('genre', this.state.genre)
        console.log(data)
        axios.post("http://localhost:5000/gen_text", data).then(res => {
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
                <button type="button" className="btn btn-primary" onClick={this.generate}>Generate Story</button>
                {
                    this.state.display_str !== '' ? 
                    <h1> {this.state.display_str} </h1>
                    :
                    <h1> didn't generate text yet :( </h1>
                } 
            </div>
        )
    }
}

export default GenTextInput;