

import { useState, useEffect, type FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import { getTask, createTask, updateTask, deleteTask, getTasks } from "../api/task";
import type { Task } from "../types";
import { ApiError } from "../api/client";


export default function Dashboard() {
    const { user, logout } = useAuth();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [title, setTitle] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

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

    return (
        <div className="min-h-screen bg-gray-100 px-4 py-8">
            <div className="max-w-lg mx-auto">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold text-gray-800">{user?.email}'s Taks</h1>
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
                        {tasks.map((task) => (
                            <li 
                                key={task.id}
                                className="bg-white rounded shadow-sm px-4 py-3 flex items-center justify-between"
                            >
                                <label className="flex items-center gap-3 cursor-pointer flex-1">
                                    <input 
                                        type="checkbox"
                                        checked={task.completed}
                                        onChange={() => handleToggle(task)}
                                        className="h-4 w-4"
                                    />
                                    <span
                                        className={
                                            task.completed? 'line-through text-gray-400' : 'text-gray-800'
                                        }
                                        >
                                            {task.title}
                                    </span>
                                </label>
                                <button
                                    onClick={() => handleDelete(task.id)}
                                    className="text-sm text-red-500 hover:underline ml-3"
                                >
                                    Delete
                                </button>
                            </li>
                        ))}
                    </ul>
                )}

            </div>
        </div>
    )

}



