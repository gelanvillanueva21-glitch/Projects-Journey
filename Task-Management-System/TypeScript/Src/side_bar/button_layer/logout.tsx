

import type { ButtonProps } from "../props";


export function LogOutButton({onClick: clickHandler}: ButtonProps) {
    return (
        <button onClick={clickHandler}>
            LogOut.
        </button>
    )
}




