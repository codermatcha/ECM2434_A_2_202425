import React, { useEffect, useState } from "react";

const Home = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    console.log("Home component mounted!"); // ✅ Check if Home is rendering
    fetch("/api/tasks")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched tasks:", data); // ✅ Log API response
        setTasks(data);
      })
      .catch((error) => console.error("Error fetching tasks:", error));
  }, []);

  return (
    <div>
      <h2>Home Page</h2>
      {tasks.length > 0 ? (
        tasks.map((task, index) => <p key={index}>{task.name}</p>)
      ) : (
        <p>No tasks found</p>
      )}
    </div>
  );
};

export default Home;
