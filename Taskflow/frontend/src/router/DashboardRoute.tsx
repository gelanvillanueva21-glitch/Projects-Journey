

import { useAuth } from "../context/AuthContext";



export function DashBoard() {
    const { user, logout } = useAuth();
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="text-center">
                <p className="text-xl mb-4">Log in as {user?.email}</p>
                <button
                    onClick={logout}
                    className="bg-red-500 text-white px-4 py-2 rounded"
                >
                    Logout
                </button>
            </div>
        </div>
    )
}


