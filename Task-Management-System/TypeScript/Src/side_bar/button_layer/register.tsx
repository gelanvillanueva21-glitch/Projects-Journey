

import type { ButtonProps } from "../props";



export function RegisterButton({onClick: clickHandler}: ButtonProps) {
    return (
        <button onClick={clickHandler}>
            Register.
        </button>
    )
}

