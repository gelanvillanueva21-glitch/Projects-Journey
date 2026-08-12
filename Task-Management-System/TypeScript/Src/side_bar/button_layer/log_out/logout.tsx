

import type { ButtonProps } from "../../props"


export function LogOutButton({onClick}: ButtonProps) {
    return (
        <button className="sidebar-button" onClick={onClick}>
            LogOut.
        </button>
    )
}




