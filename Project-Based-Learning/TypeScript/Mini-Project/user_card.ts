

interface UserProfile{
    username : string,
    role : "admin" | "editor" | "viewer",
    isActive : boolean
}



function UserCard(props : UserProfile) {

    const status = props.isActive ? "Active" : "Inactive";
    return `[User : ${props.username}]-[Role : ${props.role}]-[Active : ${status}]`;

}


let userInfo : UserProfile = {
    username : "Gelan.mar",
    role : "admin",
    isActive : false
};
console.log(UserCard(userInfo));


export default UserCard



