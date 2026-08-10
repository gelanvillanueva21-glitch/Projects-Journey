

import { type Profile } from "./Profile";


const JWToken = () => {
    if (localStorage.length === 1) 
        return localStorage.getItem("JWT");
    return null;
}



export default JWToken;

