import React, { useEffect, useState } from "react";

function TaskList() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Check if this runs
    console.log("Fetching tasks...");

    fetch("http://127.0.0.1:5000/tasks")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched tasks:", data);
        setTasks(data);
      })
      .catch((err) => console.error("Error fetching tasks:", err));
  }, []);

  return (
    <div>
      <h2>Task List</h2>
      <ul>
        {tasks.length === 0 ? (
          <li>No tasks found</li>
        ) : (
          tasks.map((task) => (
            <li key={task.id}>
              {task.title}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default TaskList;