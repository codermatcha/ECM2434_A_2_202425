import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Profile = () => {
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();  // ✅ Navigation function

    useEffect(() => {
        const fetchProfile = async () => {
            const token = localStorage.getItem("access_token");  // ✅ Get JWT token
            const username = localStorage.getItem("username");  // ✅ Get username

            if (!token || !username) {
                navigate("/login");  // ✅ If no token, redirect to login
                return;
            }

            const response = await fetch("http://127.0.0.1:8000/api/profile/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`  // ✅ Send token for authentication
                }
            });

            const data = await response.json();
            if (response.ok) {
                setProfileData(data);
            } else {
                console.error("Failed to fetch profile:", data);
                navigate("/login");  // ✅ If API fails, redirect to login
            }
            setLoading(false);
        };

        fetchProfile();
    }, [navigate]);

    if (loading) return <p>Loading profile...</p>;

    return (
        <div>
            <h2>Welcome, {profileData.username}!</h2>
            <p>Total Points: {profileData.total_points}</p>

            <h3>Your Bingo Board</h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "10px" }}>
                {profileData.all_tasks.map((task) => (
                    <div
                        key={task.id}
                        style={{
                            padding: "20px",
                            border: "2px solid black",
                            textAlign: "center",
                            backgroundColor: profileData.completed_tasks.includes(task.id) ? "green" : "white",
                            color: profileData.completed_tasks.includes(task.id) ? "white" : "black",
                            fontWeight: "bold"
                        }}
                    >
                        {task.description}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Profile;
