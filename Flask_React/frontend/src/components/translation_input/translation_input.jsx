import React, { Component } from "react"
import './translation_input.css';
import axios from 'axios';

class TranslationInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selected_file: null,
            display_str: '',
            new_input: false,
            done_uploading: false,
            sentence: ''
        }
    }

    updateFile = event => {
        console.log(event.target.files[0]);
        this.setState({
            selected_file: event.target.files[0]
        })

    }

    getAnotherVid = () => {
        this.setState({
            new_input: true
        })

    }

    doneUploadingVid = () => {
        // translate word to sentence now 
        this.setState({
            done_uploading: true
        })

        const data = new FormData();
        data.append('input', this.state.display_str)
        console.log(data)
        axios.post("http://localhost:5000/w2s", data).then(res => {
            console.log(res);
            this.setState({
                sentence: res.data
            })
        }
        )

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
                display_str: this.state.display_str + res.data + ' ',
                responseStatusOK: (res.status === 200),
                new_input: false
            })
        })
    }


    render() {
        return (

            <div>
                {
                    this.state.display_str === '' ?
                        <div>
                            <input type="file" className="form-control" multiple="" onChange={this.updateFile} />
                            <button type="button" className="btn-submit" onClick={this.getTranslation}>Submit Video</button>
                        </div>
                        :

                        <div>
                            {
                                this.state.sentence === '' ?

                                    this.state.new_input ?
                                        <div>
                                            <h1> Inputting next video  </h1>
                                            <input type="file" className="form-control" multiple="" onChange={this.updateFile} />
                                            <button type="button" className="btn btn-success btn-block" onClick={this.getTranslation}>Get Word Level Translation</button>
                                        </div>
                                        :
                                        <div>
                                            <h1> Translated last video, waiting for next move </h1>
                                            <h1> {this.state.display_str} </h1>
                                            <button type="button" className="btn btn-success btn-block" onClick={this.getAnotherVid}>Upload Another Video</button>
                                            <button type="button" className="btn btn-success btn-block" onClick={this.doneUploadingVid}>Done Uploading</button>
                                        </div>

                                    :

                                    <div>
                                        <h1>Got sentence translation</h1>
                                        <h1> {this.state.sentence}</h1>
                                    </div>
                            }
                        </div>
                }
            </div>
        )
    }
}

export default TranslationInput;