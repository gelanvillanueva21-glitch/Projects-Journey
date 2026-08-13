


import type { ButtonProps } from "../../types/props";
import linkedinIcon from "../icons/linkedin-svgrepo.svg";



export function LinkedinButton({onClick}: ButtonProps) {
    return (
        <button
            className="social-media-button"
            onClick={onClick}>
            <img 
                src={linkedinIcon} 
                alt="Linkedin Logo" />
        </button>
    )
}

