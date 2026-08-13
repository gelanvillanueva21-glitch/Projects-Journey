

import type { ButtonProps } from "../../../types/props"


export function LogOutButton({onClick}: ButtonProps) {
    return (
        <button className="sidebar-button" onClick={onClick}>
            LogOut.
        </button>
    )
}




