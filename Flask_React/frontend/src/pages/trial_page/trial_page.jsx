import React, { Component } from 'react';
import Uploader from '../../components/uploader.jsx';
import NavBar from '../../components/navbar/navbar.jsx';

class TrialPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <Uploader />
            </div>
        );
    }
}

export default TrialPage;