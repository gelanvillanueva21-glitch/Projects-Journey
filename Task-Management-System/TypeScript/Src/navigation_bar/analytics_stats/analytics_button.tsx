

import type { ButtonProps } from "../../types/props";
import analyticsLogo from "../icons/bar-chart.svg"



export function AnalyticsButton({onClick}: ButtonProps) {
    return (
        <button 
            id="analytics-button"
            onClick={onClick}>
            <img 
                src={analyticsLogo} 
                alt="Bar Chart Logo" />
            Analytics
        </button>
    )
}




