

import {type Task} from "./TaskTypes";


interface Auth {
    authorization: string;
}


export interface Profile {
    profilePicture?: string;
    token: Auth;
    name: string;
    taskList: Task[];
}



