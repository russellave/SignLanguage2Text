import React, { Component } from 'react';
import './App.css';
import Uploader from './components/uploader.jsx';

class App extends Component {
    // initialize our state


    // here is our UI
    // it is easy to understand their functions when you
    // see them render into our screen
    render() {
        return (
            <Uploader/>
            );
    }
}

export default App;