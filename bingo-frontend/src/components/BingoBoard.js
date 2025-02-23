import React, { useEffect, useState } from "react";
import axios from "axios";
import "./bingoboard.css";  
import { useNavigate } from "react-router-dom";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const BingoBoard = () => {
  const [tasks, setTasks] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_URL}/tasks/`)
      .then(response => {
        console.log("Tasks fetched:", response.data);
        setTasks(response.data);
      })
      .catch(error => console.log(error));
  }, []);

  const handleTaskClick = (task) => {
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

  return (
    <div className="bingo-container">
        <h1 className="bingo-header">Bingo Board</h1>
        <div className="bingo-board">
        {tasks.map((task, index) => (
          <div
              key={task.id}
              className={`bingo-cell ${task.completed ? "completed" : ""}`}
              onClick={() => handleTaskClick(task)} // Added onClick handler
            >
              <div className="cell-content">
                <div className="points">{task.points} marks</div>
                <div className="description">{task.description}</div>
                {task.requiresUpload && <div className="upload-indicator">📷</div>}
                {task.requireScan && <div className="scan-indicator">🤳🏻</div>}
              </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BingoBoard;
