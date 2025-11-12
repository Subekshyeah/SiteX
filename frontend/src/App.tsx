import LoginPage from "./Pages/LoginPage";
import RegisterPage from "./Pages/RegisterPage";

import { Route, Routes } from 'react-router-dom';

import Home from './Pages/Home';

//Futsal Admin
import CreateFutsal from './Pages/FutAdmin/CreateFutsal';


const App = () => {
    return (
        <Routes>
            <Route path='/' element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<div>Welcome to the Landing Page!</div>} />
            {/* Futsal Admin Routes */}
            <Route path="/futadmin/create-futsals" element={<CreateFutsal />} />
        </Routes>
    );
};

export default App;
