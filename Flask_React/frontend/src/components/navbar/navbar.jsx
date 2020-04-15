import React, { Component } from "react"
import './navbar.css';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

class NavBar extends Component {

    render() {
        return (

            <div>
                <Navbar className="nav" sticky="top">
                    <Navbar.Brand href="/" className="navtext"
                        style={{color:"white"}}
                    >
                        ASL to Text
                    </Navbar.Brand>
                    <Nav className="mr-auto">
                        <Nav.Link href="/translate" className="navtext"
                            style={{color:"white"}}
                        >
                            Translator
                        </Nav.Link>
                        <Nav.Link href="/info" className="navtext"
                            style={{color:"white"}}
                        >
                            How it works
                        </Nav.Link>
                    </Nav>
                </Navbar>
            </div>
        )
    }
}

export default NavBar;