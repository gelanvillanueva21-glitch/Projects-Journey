
import React from "react";
import IconTitle from "./icon_title_layer/Title";
import { ProfileLayer } from "./profile_layer/profile";
import type { ProfileProps } from "./props";



function SideBarLayer({profilePicture, name}: ProfileProps): React.JSX.Element {

    return (
        <section id="side-bar">
            <IconTitle/>
            <ProfileLayer 
                profilePicture={profilePicture}
                name={name}/>
        </section>
    )

}


export default SideBarLayer;


