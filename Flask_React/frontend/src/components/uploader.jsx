import React, { Component } from "react"


import axios from 'axios';

var Base64 = require('js-base64').Base64;

function wait(ms){
    var start = new Date().getTime();
    var end = start;
    while(end < start + ms) {
      end = new Date().getTime();
   }
 }

class Uploader extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedFile: null,
            responseStatusOK: false,
            returnedFile: null, 
            name: '', 
            display_str: ''
        }
    }

    onChangeHandler = event => {
        console.log(event.target.files[0]);
        this.setState({
            selectedFile: event.target.files[0],
            loaded: 0,
        })

    }

    onClickHandler = () => {
        console.log(this.state.selectedFile)
        const data = new FormData()
        data.append('images', this.state.selectedFile)
        axios.post("http://localhost:5000/image", data).then(res => {
            console.log(res);
            this.setState({
                returnedFile: res.data,
                responseStatusOK: (res.status === 200)
            })
        })
    }

    updateState = (event) => {
        console.log(event.target.value);
        this.setState({
            name: event.target.value
        })
    }

    sayHi = () => {
        const data = new FormData();
        data.append('name', this.state.name)
        axios.post("http://localhost:5000/caroline", data). then(res => {
            console.log(res);
            this.setState({
                display_str: res.data
            })
        }
        )

    }

    



    render() {
        if(this.state.responseStatusOK){
            wait(200)
            return <img src={require('../assets/detection.jpg')} alt="" height="300" width="300" />
        }
        else{
            return (
                < div className="container" >
                    <div className="row">
                        <div className="offset-md-3 col-md-6">

                            <div className="form-group files">
                                <label>Upload Your File </label>
                                <input type="file" className="form-control" multiple="" onChange={this.onChangeHandler} />
                            </div>
                            <button type="button" class="btn btn-success btn-block" onClick={this.onClickHandler}>Detect</button>
                            <br/>
                            <input type="text" placeholder ="Who should I say hi to?" onChange={this.updateState}/>
                            <br/>
                            <button type="button" class="btn btn-primary" onClick={this.sayHi}>Say Hi</button>
                            {
                                this.state.display_str != '' ? 
                                <h1> {this.state.display_str} </h1>
                                :
                                <h1> didn't ask me to say hi yet :( </h1>
                            }
                        </div>
                    </div>
                </div>
            )
        }
    }
}

export default Uploader;