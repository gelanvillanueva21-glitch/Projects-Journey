

import type { ButtonProps } from "../../../types/props"


export function RegisterButton({onClick}: ButtonProps) {
    return (
        <button className="sidebar-button" onClick={onClick}>
            Register.
        </button>
    )
}

