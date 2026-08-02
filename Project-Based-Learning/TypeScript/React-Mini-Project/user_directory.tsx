

import React from "react"


interface User {
    id: string;
    name: string;
    role: "admin" | "editor" | "viewer";
    isActive: boolean
}


interface UserDirectoryProps {
    users: User[];
    isLoading: boolean;
    error: string | null;
}



function UserDirectory({ users, isLoading, error}: UserDirectoryProps): React.JSX.Element {

    if (isLoading) return <p>Loading users...</p>
    if (error !== null) return <p className="error">Error: {error}</p>
    if (users.length === 0) return <p>No users found.</p>
    return (
        <ul>
            {users.map((user, index) => (
                <li 
                key={user.id} 
                className={user.isActive? 
                    "active" : "inactive"}></li>
            ))}
        </ul>
    )
}



export default UserDirectory


