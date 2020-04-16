import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import Vid2TextInput from '../../components/vid2text_input/vid2text_input.jsx';

class TranslationPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <Vid2TextInput/>
            </div>
        );
    }
}

export default TranslationPage;