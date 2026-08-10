

import React, { useState } from "react";
import type { ButtonProps } from "../props";
import JWToken from "../../types/ApiData";
import { ChangePasswordButton } from "./change_password";
import { LogOutButton } from "./logout";
import { RegisterButton } from "./register";
import { LogInButton } from "./login";




export function ButtonLayer(): React.JSX.Element {

    const isJwtExist = JWToken()
    function onClick() {

    }

    return (
        <div>
            {isJwtExist? (
                <LogOutButton onClick={onClick}/>
            ): (
                <LogInButton onClick={onClick} />
            )}
            <RegisterButton onClick={onClick} />
            <ChangePasswordButton onClick={onClick}/>
        </div>
    )
}






