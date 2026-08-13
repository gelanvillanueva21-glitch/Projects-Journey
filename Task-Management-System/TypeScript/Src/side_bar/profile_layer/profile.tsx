

import React from "react";
import type { ProfileProps } from "../../types/props";
import temporaryProfile from "./Icon/user-profile-person.svg";


export function ProfileLayer({profilePicture, name}: ProfileProps): React.JSX.Element {
    const displayProfile = profilePicture ?? temporaryProfile;
    const displayName = name ?? "Guest";

    return (
        <div className="profile-content">
            <img
                id="profile-picture" 
                src={displayProfile}
                alt="User's Profile" />
            <h3>{displayName}</h3>
        </div>
    )

}






