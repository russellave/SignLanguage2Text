import React, { Component } from "react"
import './home_page.css';
import Helmet from 'react-helmet';
import FadeIn from 'react-fade-in';


class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state={
            clicked: false
        }
    }

    onClickHandler = () => {
        this.setState({
            clicked: true
        })
    }


    render() {
        return (

            <div>
                <Helmet bodyAttributes={{ style: 'background-color : #314455' }} />
                <div className="main_title" >
                    ASL to Text Translation
                </div>
                <div className="it_subheading">
                    at the click of a button
                </div>
                <button type="button" class="btn-lg btn-lg-red"  onClick={this.onClickHandler}>Translator</button>
                <button type="button" className="btn-lg btn-lg-gray" onClick={this.onClickHandler}>How it works</button>
            </ div>
        )
    }
}

export default Home;