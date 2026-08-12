

import type { ButtonProps } from "../../props"


export function LogInButton({onClick}: ButtonProps) {

    return (
        <button className="sidebar-button" onClick={onClick}>
            Log In.
        </button>
    )
}


