import type { ButtonProps } from "../../types/props";
import instagramIcon from "../icons/instagram-svgrepo.svg";



export function InstagramButton({onClick}: ButtonProps) {
    return (
        <button
            className="social-media-button"
            onClick={onClick}>
            <img 
                src={instagramIcon} 
                alt="Instagram Logo" />
        </button>
    )
}


