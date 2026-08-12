

import type { ButtonProps } from "../../props"


export function ChangePasswordButton({onClick}: ButtonProps) {
    
    return (
        <button className="sidebar-button" onClick={onClick}>
            Change Password.
        </button>
    )
}




