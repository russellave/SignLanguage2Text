import React, { Component } from 'react';
import './App.css';
import HomePage from './pages/home_page/home_page.jsx';
import TrialPage from './pages/trial_page/trial_page.jsx'
import { Switch, Route } from 'react-router-dom';

class App extends Component {
    // initialize our state


    // here is our UI
    // it is easy to understand their functions when you
    // see them render into our screen
    render() {
        return (
            <div>
                <Switch>
                    <Route exact={true} path='/' component={HomePage} />
                    <Route exact={true} path='/trial' component={TrialPage} />
                </Switch>
            </div>
        );
    }
}

export default App;