

import type { ButtonProps } from "../props";


export function ChangePasswordButton({onClick: clickHandler}: ButtonProps) {
    return (
        <button onClick={clickHandler}>
            Change Password.
        </button>
    )
}




