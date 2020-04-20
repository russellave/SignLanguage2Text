import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import Vid2TextInput from '../../components/vid2text_input/vid2text_input.jsx';
import W2SInput from '../../components/w2s_input/w2s_input.jsx';
import TranslationInput from '../../components/translation_input/translation_input.jsx';

class TranslationPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <TranslationInput/>
                {/* <Vid2TextInput/>
                <br/>
                <W2SInput/> */}
            </div>
        );
    }
}

export default TranslationPage;