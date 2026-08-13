
import React from "react";
import IconTitle from "./icon_title_layer/Title";
import { ProfileLayer } from "./profile_layer/profile";
import type { ProfileProps } from "../types/props";
import { ButtonLayer } from "./button_layer/layer";



function SideBarLayer({profilePicture, name}: ProfileProps): React.JSX.Element {

    return (
        <section id="side-bar">
            <IconTitle/>
            <ProfileLayer 
                profilePicture={profilePicture}
                name={name}/>
            <ButtonLayer/>
        </section>
    )

}


export default SideBarLayer;


