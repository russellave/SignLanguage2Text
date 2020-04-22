import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import TransInd from '../../components/trans_ind/trans_ind.jsx'
import './info_page.css'

class InfoPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <div className="intro-text"> 
                    <p>
                    <span className='intro-text-bigger'>The ASL words to English sentence translation done on this website is broken down into three steps: </span>
                    <ul>
                        <li> <span className="intro-text-red">Video to Text</span> -<i> Videos of signed words are translated into individual English words.</i>  </li>
                        <li> <span className="intro-text-red">Words to Sentences </span>- <i>Collections of English words are translated into full English sentences. </i></li>
                        <li> <span className="intro-text-red">Generative Text </span>- <i>A starting piece of text is used to generate a story or play. </i> </li>
                    </ul>
                    The models and training data used in each of these steps is briefly explained below.  You can also try out each step individually here.  
                    For further details, see the <a href= 'https://github.com/russellave/SignLanguage2Text' target="_blank">code on GitHub </a> 
                    and <a href='https://docs.google.com/document/d/12AMnizH-Z2Du6TNWCmnrv8UApx5tf71J2Amv8QIWuag/edit?usp=sharing' target="_blank">this design document</a>.  
                    </p>
                    <hr/>
                </div>
                <TransInd/>
            </div>
        );
    }
}

export default InfoPage;