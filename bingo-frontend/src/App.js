import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserProfile from "./components/Userprofile";
import Home from "./components/Home"; // Home now includes login/register

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/profile" element={<UserProfile />} />
      </Routes>
    </Router>
  );
};

export default App;
