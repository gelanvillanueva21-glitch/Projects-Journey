

import type { ButtonProps } from "../props";


export function LogInButton({onClick: clickHandler}: ButtonProps) {
    return (
        <button onClick={clickHandler}>
            Log In.
        </button>
    )
}


