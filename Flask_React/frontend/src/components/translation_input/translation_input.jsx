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
                            <div className='file-upload'>
                                <input type="file" className="form-control-tr" multiple="" onChange={this.updateFile} />
                            </div>
                            <button type="button" className="btn-or-sub" onClick={this.getTranslation}>Submit Video</button>
                        </div>
                        :

                        <div>
                            {
                                this.state.sentence === '' ?

                                    this.state.new_input ?
                                        <div>
                                            <p className="tr-result"> Current word-level translation(s): {this.state.display_str}</p>
                                            <div className="file-upload"> 
                                                <input type="file" className="form-control-tr" multiple="" onChange={this.updateFile} />
                                            </div>
                                            <button type="button" className="btn-submit" onClick={this.getTranslation}>Submit Video</button>
                                        </div>
                                        :
                                        <div>
                                            <p className="tr-result"> Current word-level translation(s): {this.state.display_str}</p>
                                            <button type="button" className="btn-upload-another" onClick={this.getAnotherVid}>Upload Another Video</button>
                                            <button type="button" className="btn-done" onClick={this.doneUploadingVid}>Done Uploading</button>
                                        </div>

                                    :

                                    <div>
                                            <p className="tr-result"> Sentence-level translation: {this.state.sentence}</p>
                                       
                                    </div>
                            }
                        </div>
                }
            </div>
        )
    }
}

export default TranslationInput;