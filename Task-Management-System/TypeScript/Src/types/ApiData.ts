

import { account } from "./AccountData";








const JWToken = () => {
    if (localStorage.length === 1) 
        return localStorage.getItem("JWT");
    return null;
}


export function register(username: string, password: string) {
    if (username.length >= 8 && password.length >= 8) {
        return true
    }
    if (false) {
        return "message"
    }
    return null
}


export function temporaryDataFetch() {
    return account.find(
        account => account.token.authorization === JWToken()
    )
}



export default JWToken;

