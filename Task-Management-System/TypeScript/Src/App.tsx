

import React, { useState } from "react";
import SideBarLayer from "./side_bar/SideBar";
import JWToken, { temporaryDataFetch } from "./types/ApiData";


export function App(): React.JSX.Element {
    const data = temporaryDataFetch();
    return (
        <SideBarLayer 
            profilePicture={data?.profilePicture}
            name={data?.name}/>
    )

}


