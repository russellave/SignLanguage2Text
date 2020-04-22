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
            sentence: '',
            words: '',
            gen_in: '',
            gen_out: ''
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
            done_uploading: true,
            words: this.state.display_str
        })
    }

    getSentence = () => {
        const data = new FormData();
        data.append('input', this.state.words)
        console.log(data)
        axios.post("http://localhost:5000/w2s", data).then(res => {
            console.log(res);
            this.setState({
                sentence: res.data,
                gen_in: res.data
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

    updateWords = (event) => {
        this.setState({
            words: event.target.value
        })
    }

    updateGenIn = (event) => {
        this.setState({
            gen_in: event.target.value
        })
    }

    getStory = () => {
        const data = new FormData();
        data.append('input', this.state.gen_in)
        data.append('genre', 'news')
        console.log(data)
        axios.post("http://localhost:5000/gen_text", data).then(res => {
            console.log(res);
            this.setState({
                gen_out: res.data
            })
        }
        )

    }

    getPlay = () => {
        const data = new FormData();
        data.append('input', this.state.gen_in)
        data.append('genre', 'play')
        console.log(data)
        axios.post("http://localhost:5000/gen_text", data).then(res => {
            console.log(res);
            this.setState({
                gen_out: res.data
            })
        }
        )

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
                                !this.state.done_uploading ?

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

                                    this.state.gen_out === '' ?

                                    <div>
                                        <p className="tr-result tr-in">Input to words to sentence translator: </p>
                                        <input type="text" className="input-text" placeholder ={this.state.words} onChange={this.updateWords}/>
                                        <button type="button" className="btn-sent" onClick={this.getSentence}>Get Sentence-Level Translation</button>
                                        {
                                            this.state.sentence === '' ?
                                            <br/>
                                            : 
                                            <div>
                                                <p className="tr-result tr-sent"> Translation: <span className="res">{this.state.sentence}</span></p>
                                                
                                                <button type="button" className="btn-story" onClick={this.getStory}>Tell Me a Story</button>
                                                <button type="button" className="btn-play" onClick={this.getPlay}>Write Me a Play</button>
                                                starting with: <input type="text" className="input-text-gen" placeholder ={this.state.sentence} onChange={this.updateGenIn}/>
                                               
                                            </div>
                                            
                                        }
                                       
                                    </div>

                                    :

                                    <div className='gen-out'>
                                        {this.state.gen_out}
                                    </div>
                            }
                        </div>
                }
            </div>
        )
    }
}

export default TranslationInput;