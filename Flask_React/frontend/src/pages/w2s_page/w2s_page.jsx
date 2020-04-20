import React, { Component } from 'react';
import NavBar from '../../components/navbar/navbar.jsx';
import W2SInput from '../../components/w2s_input/w2s_input.jsx';

class W2SPage extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <W2SInput/>
            </div>
        );
    }
}

export default W2SPage;