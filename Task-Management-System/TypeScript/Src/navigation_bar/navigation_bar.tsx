

import type React from "react";
import { SocialMediaButton } from "./social_media_buttons/social_media";
import { AnalyticsButton } from "./analytics_stats/analytics_button";
import type { ButtonProps } from "../types/props";


export default function NavBar({onClick}: ButtonProps): React.JSX.Element {
    


    return (
        <section className="navigation-container">
            <SocialMediaButton/>
            <AnalyticsButton onClick={onClick}/>
        </section>
    )

}





