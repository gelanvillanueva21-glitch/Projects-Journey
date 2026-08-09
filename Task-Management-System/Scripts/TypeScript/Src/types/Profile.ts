

import Task from "./TaskTypes";


interface Auth {
    authorization: string;
}


interface Profile {
    profilePicture?: string;
    token: Auth;
    name: string;
    taskList: Task[];
}


export default Profile;

