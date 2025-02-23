import React, { useState } from "react";

const Register = () => {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        passwordagain: ""  // ✅ Ensure this field exists
    });

    const [message, setMessage] = useState("");

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.password !== formData.passwordagain) {
            setMessage("Passwords do not match!");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/api/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                setMessage("Registration successful! You can now log in.");
            } else {
                setMessage(data.error || "Registration failed.");
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("An error occurred. Please try again.");
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <label>Username:</label>
                <input type="text" name="username" value={formData.username} onChange={handleChange} required />

                <label>Email (@exeter.ac.uk only):</label>
                <input type="email" name="email" value={formData.email} onChange={handleChange} required />

                <label>Password:</label>
                <input type="password" name="password" value={formData.password} onChange={handleChange} required />

                <label>Confirm Password:</label>
                <input type="password" name="passwordagain" value={formData.passwordagain} onChange={handleChange} required />

                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;
