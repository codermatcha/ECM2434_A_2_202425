import React, { useEffect, useState } from "react";
import axios from "axios";
import BingoBoard from "./BingoBoard"; // ✅ Import the BingoBoard component
import "./UserProfile.css"; // Ensure styling is correct

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`${API_URL}/api/profile/`, { withCredentials: true })
            .then(response => {
                setUser(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching user profile:", error);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading profile...</p>;
    if (!user) return <p>Error loading profile.</p>;

    return (
        <div className="profile-container">
            <h1>Welcome, {user.username}!</h1>
            <p><strong>Total Points:</strong> {user.total_points}</p>
            <p><strong>Completed Tasks:</strong> {user.completed_tasks}</p>
            <p><strong>Leaderboard Rank:</strong> {user.leaderboard_rank}</p>

            {/* ✅ Embed the Bingo Board component */}
            <BingoBoard />
        </div>
    );
};

export default UserProfile;
