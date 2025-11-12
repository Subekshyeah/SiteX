import React from 'react';
import './Navbar.module.css';

const Navbar: React.FC = () => {
    return (
        <div className="navbar">
            <div className="navbar-logo">MyMapApp</div>
            <div className="navbar-buttons">
                <button className="navbar-button">Search</button>
                <button className="navbar-button">Directions</button>
                <button className="navbar-button">Menu</button>
            </div>
        </div>
    );
};

export default Navbar;