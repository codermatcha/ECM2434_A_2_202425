import React, { useEffect, useState } from "react";
import axios from "axios";
import BingoBoard from "./BingoBoard"; 
import "./Profile.css"; // ✅ Updated CSS import

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const Profile = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        console.log("Fetching user profile from API:", `${API_URL}/api/profile/`);

        axios.get(`${API_URL}/api/profile/`, { withCredentials: true })
            .then(response => {
                console.log("User profile response:", response.data);
                if (!response.data || typeof response.data !== "object") {
                    console.error("Invalid profile data:", response.data);
                    setError("Invalid profile response.");
                    setUser({});
                } else {
                    setUser(response.data);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching user profile:", error);
                setError("Failed to load profile.");
                setUser({});
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading profile...</p>;
    if (error) return <p style={{ color: "red" }}>{error}</p>;

    return (
        <div className="profile-container">
            <h1>Welcome, {user.username || "Guest"}!</h1>
            <p><strong>Total Points:</strong> {user.total_points || 0}</p>
            <p><strong>Completed Tasks:</strong> {user.completed_tasks || 0}</p>
            <p><strong>Leaderboard Rank:</strong> {user.leaderboard_rank || "N/A"}</p>

            {/* ✅ Bingo Board Integrated */}
            <BingoBoard />
        </div>
    );
};

export default Profile;
