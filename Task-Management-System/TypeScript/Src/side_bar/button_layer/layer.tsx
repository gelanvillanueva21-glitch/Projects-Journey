

import React, { useState } from "react";
import JWToken from "../../types/ApiData";
import { ChangePasswordButton } from "./change_password/change_password";
import { LogOutButton } from "./log_out/logout";
import { RegisterButton } from "./register/register";
import { LogInButton } from "./log_in/login";
import { ChangePasswordWindow } from "./change_password/change_pass_window";
import { LoginWindow } from "./log_in/login_window";
import { LogoutWindow } from "./log_out/logout_window";
import { RegisterWindow } from "./register/register_window";



export function ButtonLayer(): React.JSX.Element {
    const [activeWindow, setActiveWindow] = useState<"login" | "logout" | "register" | "change_password" | null>(null);

    const isJwtExist = JWToken()
    return (
        <>z
            <div className="sidebar-button-container">
                {isJwtExist? (
                    <>
                        <LogOutButton onClick={() => setActiveWindow("logout")}/>
                        <ChangePasswordButton onClick={() => setActiveWindow("change_password")}/>
                    </>
                ): (
                    <>
                        <LogInButton onClick={() => setActiveWindow("login")}/>
                        <RegisterButton onClick={() => setActiveWindow("register")}/>
                    </>
                )}
            </div>

            {activeWindow === "login" && (
                <LoginWindow onClose={() => setActiveWindow(null)}/>
            )}
            {activeWindow === "logout" && (
                <LogoutWindow onClose={() => setActiveWindow(null)}/>
            )}
            {activeWindow === "register" && (
                <RegisterWindow onClose={() => setActiveWindow(null)}/>
            )}
            {activeWindow === "change_password" && (
                <ChangePasswordWindow onClose={() => setActiveWindow(null)}/>
            )}
        </>
    )
}






