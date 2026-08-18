

import type { FormEvent } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext";
import { ApiError } from "../api/client";



export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>("");
    const [isSubmitting, setIsSubemitting] = useState(false);

    const { login } = useAuth()
    const navigate = useNavigate()

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        setError(null);
        setIsSubemitting(true);

        try {
            await login({ email, password });
            navigate("/");
        } catch (err) {
            if (err instanceof ApiError)
                setError(err.message);
            else
                setError('Something went wrong. Please try again.');
        } finally {
            setIsSubemitting(false);
        }
    }

    return (
            <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
                <form
                    onSubmit={handleSubmit}
                    className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm"
                >
                    <h1 className="text-2xl font-bold mb-6 text-gray-800">Log in to TaskFlow</h1>

                    {error && (
                        <div className="bg-red-50 text-red-600 text-sm px-3 py-2 rounded mb-4">
                            {error}
                        </div>
                    )}

                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                    </label>
                    <input 
                        type="email"
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Password
                    </label>
                    <input 
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full border border-gray-300 rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="w-full bg-blue-600 text-white py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
                    >
                        {isSubmitting ? 'Logging in...' : 'Log in'}
                    </button>
                </form>
            </div>
        )

}


