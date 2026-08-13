

import { useState } from "react";
import type { WindowProps } from "../../../types/props";
import { account } from "../../../types/AccountData";


export function LoginWindow({onClose}: WindowProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isAccountExist, setAccountExist] = useState(true);
    const [showPassword, setShowPassword] = useState(false);

    function login() {
        const user = account.find(
            account => account.username === username && account.password === password
        )
        if (!user) {
            setAccountExist(false);
        }
        if (user) {
            localStorage.setItem("JWT", user.token.authorization);
            window.location.reload();
        }
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
                <form 
                    className="login-form"
                    onSubmit={(e) => {
                        e.preventDefault();
                        login();
                    }}>
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
                    {isAccountExist === false && (
                        <p className="error-message">
                            Account not found, or password/username inccorect
                        </p>
                        )}
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


