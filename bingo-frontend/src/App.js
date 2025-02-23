import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import UserProfile from "./components/Userprofile";
import Home from "./components/Home";

const App = () => {
  console.log("App component is rendering!"); // ✅ Debug message

  return (
    <Router>
      <h1>React App Loaded ✅</h1> {/* ✅ If this doesn't show, React isn't rendering */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<UserProfile />} />
      </Routes>
    </Router>
  );
};

export default App;
