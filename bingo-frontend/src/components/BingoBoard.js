import React, { useEffect, useState } from "react";
import axios from "axios";
import "./bingoboard.css";  
import { useNavigate } from "react-router-dom";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const BingoBoard = () => {
  const [tasks, setTasks] = useState([]); // ✅ Always initialize as an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Fetching tasks from API:", `${API_URL}/tasks/`);

    axios.get(`${API_URL}/tasks/`)
      .then(response => {
        console.log("API Response:", response.data);  

        if (!Array.isArray(response.data)) {
          console.error("Error: Expected an array but got:", response.data);
          setError("Invalid response from server.");
          setTasks([]);  // ✅ Ensure tasks is always an array
        } else {
          setTasks(response.data);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching tasks:", error);
        setError("Failed to load tasks.");
        setTasks([]);  // ✅ Set tasks to an empty array if there's an error
        setLoading(false);
      });
  }, []);

  const handleTaskClick = (task) => {
    if (!task) return;

    if (task.requiresUpload) {
      localStorage.setItem("selectedChoice", task.description);
      navigate("/upload");
    } else if (task.requireScan) {
      localStorage.setItem("selectedChoice", task.description);
      navigate("/scan");
    } else {
      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        )
      );
    }
  };

  if (loading) return <p>Loading Bingo Board...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="bingo-container">
        <h1 className="bingo-header">Bingo Board</h1>
        <div className="bingo-board">
          {tasks.length > 0 ? (  
            tasks.map((task) => (
              <div
                  key={task.id}
                  className={`bingo-cell ${task.completed ? "completed" : ""}`}
                  onClick={() => handleTaskClick(task)}
              >
                  <div className="cell-content">
                    <div className="points">{task.points} marks</div>
                    <div className="description">{task.description}</div>
                    {task.requiresUpload && <div className="upload-indicator">📷</div>}
                    {task.requireScan && <div className="scan-indicator">🤳🏻</div>}
                  </div>
              </div>
            ))
          ) : (
            <p>No tasks available.</p>
          )}
      </div>
    </div>
  );
};

export default BingoBoard;
