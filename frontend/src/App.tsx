import React from 'react';
import Map from './components/Map/Map';
import Sidebar from './components/Sidebar/Sidebar';
import Navbar from './components/Navbar/Navbar';
import './styles/globals.css';

const App: React.FC = () => {
    return (
        <div className="app-container">
            <Navbar />
            <div className="main-content">
                <Sidebar />
                <Map />
            </div>
        </div>
    );
};

export default App;