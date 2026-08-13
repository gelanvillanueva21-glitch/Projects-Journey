


import type { ButtonProps } from "../../types/props";
import tiktokIcon from "../icons/tiktok-svgrepo.svg";



export function TiktokButton({onClick}: ButtonProps) {
    return (
        <button
            className="social-media-button"
            onClick={onClick}>
            <img 
                src={tiktokIcon}
                alt="Tiktok Logo" />
        </button>
    )
}

