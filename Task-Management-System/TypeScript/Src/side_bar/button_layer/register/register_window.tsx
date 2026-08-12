

import { useState } from "react";
import type { WindowProps } from "../../props";
import { register } from "../../../types/ApiData";



export function RegisterWindow({onClose}: WindowProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showMessage, setMessage] = useState(false);
    const [erroMessage, setErrorMessage] = useState("");

    function registerAccount() {
        const registerStatus = register(username, password);
        
        if (!registerStatus) {
            setErrorMessage("Incorrect Pattern, username and password must be 8 characters");
            setMessage(true);
        }

        if (registerStatus === "message") {
            const temporaryMessage = "Account already exist";
            setErrorMessage(temporaryMessage);
            setMessage(true);
        }

        if (registerStatus) {
            window.location.reload();
        }

    }

    return (
        <div className="register-overlay">
            <div className="register-window">
                <div className="register-header">
                    <h2>Register</h2>
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
                    className="register-form"
                    onSubmit={(e) => {
                        e.preventDefault()
                        registerAccount()
                    }}>
                    <div className="register-input">
                        <label htmlFor="username">Username</label>
                        <input 
                            type="text"
                            id="username-input"
                            name="username"
                            placeholder="gelangwapo123"
                            onChange={(e) => setUsername(e.target.value)} />
                    </div>
                    <div className="register-input">
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
                    {showMessage === true && (
                        <p>{erroMessage}</p>
                    )}
                    <button
                        type="button"
                        className="show-password-button"
                        onClick={() => setShowPassword(prev => !prev)}>
                            {showPassword? "Show Password" : "Hide Password"}
                    </button>
                    <button
                        type="submit"
                        className="register-button"
                        onClick={registerAccount}>
                            Register
                    </button>
                </form>
            </div>
        </div>
    )
}


