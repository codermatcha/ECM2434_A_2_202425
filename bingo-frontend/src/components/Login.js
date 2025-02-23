import React, { useState } from "react";
import { useNavigate } from "react-router-dom";  // ✅ Import useNavigate

const Login = () => {
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    });

    const [message, setMessage] = useState("");
    const navigate = useNavigate();  // ✅ Navigation function for redirecting

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("access_token", data.access);  // ✅ Store JWT token
                localStorage.setItem("username", data.user);  // ✅ Store username
                setMessage("Login successful! Redirecting...");

                setTimeout(() => {
                    navigate("/profile");  // ✅ Redirect to profile page
                }, 1000);
            } else {
                setMessage(data.error || "Login failed.");
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("An error occurred. Please try again.");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <label>Username:</label>
                <input type="text" name="username" value={formData.username} onChange={handleChange} required />

                <label>Password:</label>
                <input type="password" name="password" value={formData.password} onChange={handleChange} required />

                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
