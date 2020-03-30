import React, { Component } from 'react';
import './App.css';
import Uploader from './components/uploader.jsx';
import Uploader_2 from './components/uploader_2.jsx';
import Home from './pages/home_page/home_page.jsx';

class App extends Component {
    // initialize our state


    // here is our UI
    // it is easy to understand their functions when you
    // see them render into our screen
    render() {
        return (
            <Home />
        );
    }
}

export default App;