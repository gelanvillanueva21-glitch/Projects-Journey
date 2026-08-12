

import {type Task} from "./TaskTypes";


interface Auth {
    authorization: string;
}


export interface Account {
    profilePicture?: string;
    token: Auth;
    name: string;
    taskList: Task[];
    username: string;
    password: string;
}



