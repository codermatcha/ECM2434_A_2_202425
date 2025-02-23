import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";  // ✅ Import Profile component

const Home = () => {
    return (
        <div>
            <h1>Welcome to the Bingo App</h1>
            <p>Earn points by completing sustainability tasks!</p>
            <Link to="/register">Register</Link> | 
            <Link to="/login">Login</Link> | 
            <Link to="/profile">Profile</Link>
        </div>
    );
};

const API_URL = "http://127.0.0.1:8000";  // Ensure this matches your Django backend

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/profile" element={<Profile />} />  {/* ✅ Ensure /profile exists */}
            </Routes>
        </Router>
    );
};

export default App;
