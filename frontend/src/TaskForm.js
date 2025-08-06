import { useState } from "react";

function TaskForm({ onTaskCreated }) {
  const [title, setTitle] = useState("");

  const handleSubmit = async (e) => {
  e.preventDefault();
  const newTask = { title };

  try {
    const response = await fetch("http://127.0.0.1:5000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newTask),
    });

    if (!response.ok) throw new Error("Failed to create task");

    const createdTask = await response.json(); // receives { id, title }
    onTaskCreated(createdTask);                // passes the new task to App.js
    setTitle("");                              // clear the input field
  } catch (error) {
    console.error("Error creating task:", error);
  }
};

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        placeholder="Enter new task"
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <button type="submit">Add Task</button>
    </form>
  );
}

export default TaskForm;