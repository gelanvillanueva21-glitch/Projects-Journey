

import React, { useState } from "react";
import JWToken from "../../types/ApiData";
import { ChangePasswordButton } from "./change_password/change_password";
import { LogOutButton } from "./log_out/logout";
import { RegisterButton } from "./register/register";
import { LogInButton } from "./log_in/login";




export function ButtonLayer(): React.JSX.Element {
    const [activeWindow, setActiveWindow] = useState<"login" | "logout" | "register" | "change_password" | null>(null);

    const isJwtExist = JWToken()
    return (
        <>
            <div>
                {isJwtExist? (
                    <LogOutButton onClick={() => setActiveWindow("logout")}/>
                ): (
                    <LogInButton onClick={() => setActiveWindow("login")}/>
                )}
                <RegisterButton onClick={() => setActiveWindow("register")}/>
                <ChangePasswordButton onClick={() => setActiveWindow("register")}/>
            </div>

            {activeWindow === "login" && (
                <div></div>
            )}
            {activeWindow === "logout" && (
                <div></div>
            )}
            {activeWindow === "register" && (
                <div></div>
            )}
            {activeWindow === "change_password" && (
                <div></div>
            )}
        </>
    )
}






