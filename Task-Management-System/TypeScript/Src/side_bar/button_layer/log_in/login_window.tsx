

import { useState } from "react";
import type { WindowProps } from "../../props";
import { account } from "../../../types/AccountData";


export function LoginWindow({onClose}: WindowProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isExist, setIsExist] = useState(true);
    const [showPassword, setShowPassword] = useState(false);

    function login() {
        const user = account.find(
            account => account.username === username && account.password === password
        )
        if (!user) {
            setIsExist(false);
            return false;
        } else 
            return true;
    }

    return (
        <div className="login-overlay">
            <div className="login-window">
                <div className="login-header">
                    <h2>Log In</h2>
                    <button
                        type="button"
                        className="close-button"
                        onClick={onClose}
                        aria-label="Close"
                    >
                        &times;
                    </button>
                </div>
                <form className="login-form">
                    <div className="login-input">
                        <label htmlFor="username">Username</label>
                        <input 
                            type="text"
                            id="username-input"
                            placeholder="gelangwapo"
                            name="username"
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="login-input">
                        <label htmlFor="password">Password</label>
                        <input 
                            type={showPassword? "text" : "password"} 
                            id="password-input"
                            placeholder="************"
                            name="password"
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    {isExist? (
                        <p className="error-message">
                        Account not found, or password/username inccorect
                    </p>
                    ) : ""}
                    <button
                        type="button"
                        className="show-password-button"
                        onClick={() => setShowPassword(prev => !prev)}
                        >
                        {showPassword? "Show Password" : "Hide Password"}
                    </button>
                    <button
                        type="submit"
                        className="login-button"
                        onClick={login}
                    >
                        Log In.
                    </button>
                </form>
            </div>
        </div>
    )
}


