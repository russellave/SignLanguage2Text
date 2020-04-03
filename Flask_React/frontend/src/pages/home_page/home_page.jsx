import React, { Component } from "react"
import './home_page.css';
import Helmet from 'react-helmet';

class HomePage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
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
                <div className="main-title" >
                    ASL to Text Translation
                </div>
                <div className="it-subheading">
                    at the click of a button
                </div>
                <a href="/trial">
                    <button type="button" class="btn-lg btn-lg-red">
                        Translator
                    </button>
                </a>
                <button type="button" className="btn-lg btn-lg-gray" >How it works</button>
            </ div >
        )
    }
}

export default HomePage;