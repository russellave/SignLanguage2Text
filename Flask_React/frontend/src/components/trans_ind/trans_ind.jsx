import React, { Component } from "react"
import './trans_ind.css';
import axios from 'axios';

class TransInd extends Component {
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



    resetVid2Text = () => {
        this.setState({
            selected_file: null,
            display_str: '',
            new_input: false
        })
    }

    resetAll = () => {
        this.setState({
            selected_file: null,
            display_str: '',
            new_input: false,
            done_uploading: false,
            sentence: '',
            words: '',
            gen_in: '',
            gen_out: ''
        })
    }

    resetW2S = () => {
        this.setState({
            sentence: '',
            words: this.state.display_str
        })
    }


    resetGenText = () => {
        this.setState({
            gen_in: '',
            gen_out: ''
        })
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
                words: this.state.display_str + res.data + ' ',
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
                <div className="intro-text-title">
                    <p>Video to Text</p>
                </div>
                <div className="body-text">
                    <p>This step aims to translate sign language at the word level.  This means that one signed word is translated to 
                        one corresponding English word.  <br/>
                        The model used to address this problem is an Inflated 3D ConvNet (I3D) with Inception modules pretrained on ImageNet.  
                        The training data used was the MSASL dataset.  <br/>
                        <br/>
                        To try it, upload a video of a sign below.  You will be given the word-level translation of it, 
                        and you will be able to upload another video once the first translation is returned if desired.  
                    </p>
                </div>
                {/* {All of video to text is in this block */
                    this.state.display_str === '' ?
                        <div>
                            <div className='file-upload'>
                                <input type="file" className="form-control-tr" multiple="" onChange={this.updateFile} />
                            </div>
                            <button type="button" className="btn-or-sub" onClick={this.getTranslation}>Submit Video</button>
                        </div>
                    :
                        this.state.new_input ?
                            <div>
                                <p className="tr-result"> Current Word-Level Translation(s): {this.state.display_str}</p>
                                <div className="file-upload"> 
                                    <input type="file" className="form-control-tr" multiple="" onChange={this.updateFile} />
                                </div>
                                <button type="button" className="btn-submit" onClick={this.getTranslation}>Submit Video</button>
                            </div>
                        :
                            <div>
                                <p className="tr-result2"> Current word-level translation(s): {this.state.display_str}</p>
                                <button type="button" className="btn-upload-another2" onClick={this.getAnotherVid}>Upload Another Video</button>
                                <br/>
                                <button type="button" className="btn-reset-vid2text" onClick={this.resetVid2Text}>Reset Video to Text</button>
                            </div>
                        
                }

                <div className="lr-mar">
                    <hr/>
                </div>
                <div className="intro-text-title">
                    <p>Words to Sentence</p>
                </div>
                <div className="body-text">
                    <p>This step aims to convert several word-level translations of signs into a sentence-level translation.  
                        A collection of English words that might be found in the word-level translations of a signed sentence are translated
                        into a coherent English sentence.  <br/>
                        The model used to address this problem is an RNN Encoder-Decoder model trained on a custom adaptation of a closed captions dataset.  
                        <br/>
                        <br/>
                        To try it, input several English words in the box below.  If you have done a Video to Text translation above, the result will be 
                        autofilled into the Words to Sentence input box.  
                    </p>
                </div>
                {/* All of word to sentence is in this block */
                <div>
                    <input type="text" className="input-text" placeholder ={this.state.display_str} onChange={this.updateWords}/>
                    <br/>
                    <button type="button" className="btn-sent2" onClick={this.getSentence}>Get Sentence-Level Translation</button>
                    {
                        this.state.sentence === '' ?
                        <br/>
                        : 
                        <div>
                            <br/>
                            <p className="tr-sent"> Sentence-Level Translation: <span className="res">{this.state.sentence}</span></p>
                            <button type="button" className="btn-reset-w2s" onClick={this.resetW2S}>Reset Words to Sentence</button>
                        </div>
                        
                    }
                   
                </div>
                }

                <div className="lr-mar">
                    <hr/>
                </div>
                <div className="intro-text-title">
                    <p>Generative Text</p>
                </div>
                <div className="body-text">
                    <p>This step takes an input text and generates either a story or a section of a play starting with that text.    
                        <br/>
                        The model used in this step is GPT-2, a transformer model pretrained on a vast body of text.  
                        For the story and play generation, it was trained on two datasets: one of Shakespeare plays and the other of news stories.    
                        <br/>
                        <br/>
                        To try it, input any text in the box below.  If you have done a Words to Sentence translation above, the result will be 
                        autofilled into the Generative Text input box.  
                    </p>
                </div>
                {/* All of generative text goes here */
                <div>
                    
                    <input type="text" className="input-text-gen" placeholder ={this.state.sentence} onChange={this.updateGenIn}/>
                    <br/>
                    <button type="button" className="btn-story" onClick={this.getStory}>Tell Me a Story</button> 
                    <button type="button" className="btn-play" onClick={this.getPlay}>Write Me a Play</button>
                    
                    {this.state.gen_out === '' ?
                    <br/>
                    :
                    <div>
                        <div className='gen-out'>
                            {this.state.gen_out}
                        </div>  
                        <button type="button" className="btn-reset-gen" onClick={this.resetGenText}>Reset Generative Text</button>
                    </div>
                    }    
                </div>              
                }
            </div>
        )
    }
}

export default TransInd;