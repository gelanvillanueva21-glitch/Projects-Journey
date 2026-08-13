

import React, { useState } from "react";
import SideBarLayer from "./side_bar/SideBar";
import NavBar from "./navigation_bar/navigation_bar";
import JWToken, { temporaryDataFetch } from "./types/ApiData";


export function App(): React.JSX.Element {
    const data = temporaryDataFetch();

    function analyticsClick() {

    }


    return (
        <>
            <NavBar onClick={analyticsClick}/>
            <SideBarLayer 
                profilePicture={data?.profilePicture}
                name={data?.name}/>
        </>
    )

}


