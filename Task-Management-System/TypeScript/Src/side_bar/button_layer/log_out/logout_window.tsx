

import { useState } from "react";
import type { WindowProps } from "../../../types/props";



export function LogoutWindow({onClose}: WindowProps) {

    function logout() {
        localStorage.clear();
        window.location.reload();
    }
    return (
        <div className="logout-overlay">
            <div className="logout-content">
                <h2>Are you sure you want to log out?</h2>
                <button
                    className="secondary-logout-button" 
                    onClick={onClose}>
                    No
                </button>
                <button 
                    className="primary-logout-button"
                    onClick={logout}>
                    Yes
                </button>
            </div>
        </div>
    )
}

