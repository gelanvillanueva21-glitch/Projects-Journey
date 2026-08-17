

export interface Task {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
    owner_id: number;
    created_at: string;
    updated_at: string;
}


export interface TaskCreate {
    title: string;
    description?: string;
    completed?: boolean;
}


export interface TaskUpdate {
    title?: string;
    description?: string;
    completed?: boolean;
}


export interface User {
    id: number;
    email: string;
    full_name: string | null;
    is_active: boolean;
}


export interface LoginPayload {
    email: string;
    password: string;
}


export interface RegisterPayload {
    email: string;
    password: string;
    full_name?: string;
}


