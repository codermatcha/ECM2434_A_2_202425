import React, { useState } from "react";
import Login from "./Login";
import Register from "./Register";

const Home = () => {
  const [showLogin, setShowLogin] = useState(true); // Toggle between login & register

  return (
    <div>
      <h2>Welcome to the Bingo Game!</h2>

      {/* Toggle between Login and Register Forms */}
      <button onClick={() => setShowLogin(true)}>Login</button>
      <button onClick={() => setShowLogin(false)}>Register</button>

      {/* Show Login or Register based on state */}
      {showLogin ? <Login /> : <Register />}
    </div>
  );
};

export default Home;
