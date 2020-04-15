import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';

class InfoPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                This page will have information about the data and models used.
            </div>
        );
    }
}

export default InfoPage;