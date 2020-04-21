import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import Vid2TextInput from '../../components/vid2text_input/vid2text_input.jsx';
import W2SInput from '../../components/w2s_input/w2s_input.jsx';
import TranslationInput from '../../components/translation_input/translation_input.jsx';
import './translation_page.css';


class TranslationPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <br/>
                <div className="intro-text">
                    <p> 
                    To translate from ASL to English, upload a video of an ASL sign below.  
                    Once each video is uploaded and translated at the word level, you will be able to upload another if desired.  
                    When you have finished uploading all the videos, hit <i>Done Uploading</i> to get the sentence level translation section.  
                    </p>
                    <hr/>
                </div>
                <br/>
                <TranslationInput/>
                {/* <Vid2TextInput/>
                <br/>
                <W2SInput/> */}
            </div>
        );
    }
}

export default TranslationPage;