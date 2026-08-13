

import { useState } from "react";
import type { WindowProps } from "../../../types/props";
import { account } from "../../../types/AccountData";
import JWToken from "../../../types/ApiData";


export function ChangePasswordWindow({onClose}: WindowProps) {
    const [showPassword, setShowPassword] = useState(false);
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");


    function temporaryChangePassword() {
        const token = JWToken();
        const data = account.find(
            account => account.token.authorization === token
        )
        if (data?.password === currentPassword && newPassword === confirmNewPassword) {
            data.password = currentPassword;
            window.location.reload();
        }
    }

    
    return (
        <div className="password-overlay" id="password-window">
            <div className="password-window">
                <div className="password-header">
                <h2>Change Password</h2>

                <button
                    type="button"
                    className="close-button"
                    onClick={onClose}
                    aria-label="Close"
                >
                    &times;
                </button>
                </div>

                <form 
                    className="password-form"
                    onSubmit={(e) => {
                        e.preventDefault();
                        temporaryChangePassword();
                    }}>
                <div className="input-group">
                    <label htmlFor="current-password">Current Password</label>
                    <input
                    type={showPassword? "text" : "password"}
                    id="current-password"
                    name="currentPassword"
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    placeholder="Enter current password"
                    required
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="new-password">New Password</label>
                    <input
                    type={showPassword? "text" : "password"}
                    id="new-password"
                    name="newPassword"
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Enter new password"
                    required
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="confirm-password">Confirm New Password</label>
                    <input
                    type={showPassword? "text" : "password"}
                    id="confirm-password"
                    name="confirmNewPassword"
                    onChange={(e) => setConfirmNewPassword(e.target.value)}
                    placeholder="Confirm new password"
                    required
                    />
                </div>

                <button
                    type="button"
                    className="show-password-button"
                    onClick={() => setShowPassword(prev => !prev)}
                >
                    {showPassword? "Show Password" : "Hide Password"}
                </button>

                <button 
                    type="submit" 
                    className="change-password-button"
                    onClick={temporaryChangePassword}
                >
                    Change Password
                </button>
                </form>
            </div>
        </div>
    )

}




