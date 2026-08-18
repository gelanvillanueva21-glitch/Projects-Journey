

import { useState, useEffect, type FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import { createTask, updateTask, deleteTask, getTasks } from "../api/task";
import type { Task } from "../types";
import { ApiError } from "../api/client";


export default function Dashboard() {
    const { user, logout } = useAuth();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [title, setTitle] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
    const [editTitle, setEditTitle] = useState('');
    const [editDescription, setEditDescription] = useState('');

    useEffect(() => {
        getTasks().then(setTasks)
            .catch(() => setError('Failed to load tasks'))
            .finally(() => setIsLoading(false))
    }, [])

    async function handleCreate(e: FormEvent) {
        e.preventDefault();
        if (!title.trim())
            return

        try{
            const newTask = await createTask({ title })
            setTasks([...tasks, newTask])
            setTitle('')
        } catch (err) {
            setError(err instanceof ApiError ? err.message : 'Failed to create task')
        }

    }

    async function handleToggle(task: Task) {
        try {
            const updated = await updateTask(task.id, { completed: !task.completed });
            setTasks(tasks.map((t) => (t.id === task.id ? updated : t)))
        } catch (err) {
            setError(err instanceof ApiError ? err.message : 'Failed to update task');
        }
    }

    async function handleDelete(id: number) {
        try {
            await deleteTask(id);
            setTasks(tasks.filter((t) => t.id !== id))
        } catch (err) {
            setError(err instanceof ApiError ? err.message : 'Failed to delete task')
        }
    }

    function startEditing(task: Task) {
        setEditingTaskId(task.id);
        setEditTitle(task.title);
        setEditDescription(task.description ?? '');
    }

    function cancelEditing() {
        setEditingTaskId(null);
        setEditTitle('');
        setEditDescription('');
    }

    async function handleEditSave(id: number) {
        if (!editTitle.trim()) {
            setError('Title cannot be empty');
            return
        }

        try {
            const updated = await updateTask(id, {
                title: editTitle,
                description: editDescription || undefined
            });
            setTasks(tasks.map((t) => (t.id === id ? updated : t)))
            cancelEditing()
        } catch (err) {
            setError(err instanceof ApiError ? err.message : 'Failed to update task')
        }
    }

    return (
        <div className="min-h-screen bg-gray-100 px-4 py-8">
            <div className="max-w-lg mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold text-gray-800">
                        {user?.full_name? user.full_name.split(" ")[0] : user?.email}'s Tasks
                    </h1>
                    <button
                        onClick={logout}
                        className="text-sm text-red-500 hover:underline"
                    >
                        Logout
                    </button>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 text-sm px-3 py-2 rounded mb-4">
                        {error}
                    </div>
                )}

                <form
                    onSubmit={handleCreate}
                    className="flex gap-2 mb-6"
                >
                    <input 
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="New task..."
                        className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700"
                    >
                        Add
                    </button>
                </form>

                {isLoading ? (
                    <p className="text-gray-500">Loading tasks...</p>
                ) : tasks.length === 0 ? (
                    <p className="text-gray-500">No task yet - add one above.</p>
                ) : (
                    <ul className="space-y-2">
                        {tasks.map((task) => editingTaskId === task.id ? (
                            <li
                                key={task.id}
                                className="bg-white rounded shadow-sm px-4 py-3"
                            >
                                <input 
                                    type="text"
                                    value={editTitle}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    className="w-full border border-gray-300 rounded px-2 py-1 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    placeholder="Title"
                                    autoFocus
                                />
                                <textarea 
                                    value={editDescription}
                                    onChange={(e) => setEditDescription(e.target.value)}
                                    className="w-full border border-gray-300 rounded px-2 py-1 mb-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    placeholder="Description (optional)"
                                    rows={2}
                                    />
                                <div className="flex gap-2 justify-end">
                                    <button
                                        onClick={cancelEditing}
                                        className="text-sm text-gray-500 px-3 py-1 rounded hover:bg-gray-100"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={() => handleEditSave(task.id)}
                                        className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                                    >
                                        Save
                                    </button>
                                </div>
                            </li>
                        ) : (
                            <li
                                key={task.id}
                                className="bg-white rounded shadow-sm px-4 py-3"
                            >
                                <div className="flex items-center justify-between">
                                    <label 
                                        className="flex items-center gap-3 cursor-pointer flex-1 min-w-0"
                                    >
                                        <input 
                                            type="checkbox"
                                            checked={task.completed}
                                            onChange={() => handleToggle(task)}
                                            className="h-4 w-4 shrink-0"
                                        />
                                        <span
                                            className={
                                                'trunccate ' + 
                                                (task.completed ? 'line-through text-gray-400' : 'text-gray-800')
                                            }
                                        >
                                            {task.title}
                                        </span>
                                    </label>
                                    <div className="flex gap-3 ml-3 shrink-0">
                                        <button
                                            onClick={() => startEditing(task)}
                                            className="text-sm text-blue-500 hover:underline"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            onClick={() => handleDelete(task.id)}
                                            className="text-sm text-red-500 hover:underline"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>
                                {task.description && (
                                    <p className="text-sm text-red-500 hover:underline">
                                        {task.description}
                                    </p>
                                )}
                            </li>
                        ))}
                    </ul>
                )}

            </div>
        </div>
    )

}



