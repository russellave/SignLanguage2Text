import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import GenTextInput from '../../components/gen_text_input/gen_text_input.jsx';
import './gen_text_page.css';

class GenTextPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <GenTextInput />
            </div>
        );
    }
}

export default GenTextPage;