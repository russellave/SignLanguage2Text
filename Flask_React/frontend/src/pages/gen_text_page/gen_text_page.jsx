import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import GenTextInput from '../../components/gen_text_input/gen_text_input.jsx';
import './gen_text_page.css';

class GenTextPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <h2>Shakespeare</h2>
                <GenTextInput genre="play" />

                <h2>Talk Show</h2>
                <GenTextInput genre="news" />
            </div>
        );
    }
}

export default GenTextPage;