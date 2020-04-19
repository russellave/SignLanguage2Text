import React, { Component } from 'react';
import './App.css';
import HomePage from './pages/home_page/home_page.jsx';
import TrialPage from './pages/trial_page/trial_page.jsx';
import TranslationPage from './pages/translation_page/translation_page.jsx';
import InfoPage from './pages/info_page/info_page.jsx';
import GenTextPage from './pages/gen_text_page/gen_text_page.jsx';
import { Switch, Route } from 'react-router-dom';

class App extends Component {
    
    render() {
        return (
            <div>
                <Switch>
                    <Route exact={true} path='/' component={HomePage} />
                    <Route exact={true} path='/trial' component={TrialPage} />
                    <Route exact={true} path='/translate' component={TranslationPage} />
                    <Route exact={true} path='/info' component={InfoPage} />
                    <Route exact={true} path='/gentext' component={GenTextPage} />
                </Switch>
            </div>
        );
    }
}

export default App;