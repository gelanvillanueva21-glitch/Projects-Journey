


import type { ButtonProps } from "../../types/props";
import gmailIcon from "../icons/gmail-svgrepo.svg";


export function GmailButton({onClick}: ButtonProps) {
    return (
        <button
            className="social-media-button"
            onClick={onClick}>
            <img 
                src={gmailIcon} 
                alt="Gmail Logo" />
        </button>
    )
}

