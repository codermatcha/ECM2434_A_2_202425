import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();
  
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login"); // Redirect to login if not authenticated
      return;
    }

    fetch("http://127.0.0.1:8000/api/profile/", {
      headers: { Authorization: `Token ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setUserData(data))
      .catch(() => {
        localStorage.removeItem("token");
        navigate("/login"); // Redirect on error
      });
  }, [navigate]);

  return (
    <div>
      <h2>User Profile</h2>
      {userData ? (
        <div>
          <p><strong>Username:</strong> {userData.username}</p>
          <p><strong>Email:</strong> {userData.email}</p>
          <button onClick={() => {
            localStorage.removeItem("token");
            navigate("/login");
          }}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default UserProfile;
