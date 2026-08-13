

import type { ButtonProps } from "../../../types/props"


export function LogInButton({onClick}: ButtonProps) {

    return (
        <button className="sidebar-button" onClick={onClick}>
            Log In.
        </button>
    )
}


