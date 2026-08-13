
import type { ButtonProps } from "../../types/props";
import facebookIcon from "../icons/facebook-svgrepo.svg"


export function FacebookButton({onClick}: ButtonProps) {
    return (
        <button
            className="social-media-button"
            onClick={onClick}>
            <img 
                src={facebookIcon} 
                alt="Facebook Logo" />
        </button>
    )
}


