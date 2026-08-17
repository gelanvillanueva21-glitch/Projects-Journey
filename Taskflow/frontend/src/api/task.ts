

import { request } from "./client";
import type { Task, TaskCreate, TaskUpdate } from "../types";


export function getTasks(): Promise<Task[]> {
    return request('/api/v1/tasks')
}


export function getTask(id: number): Promise<Task> {
    return request(`/api/v1/tasks/${id}`)
}


export function createTask(data: TaskCreate): Promise<Task> {
    return request(`/api/v1/tasks`, {
        method: 'POST',
        body: JSON.stringify(data)
    })
}


export function updateTask(id: number, data: TaskUpdate): Promise<Task> {
    return request(`/api/v1/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    })
}


export function deleteTask(id: number): Promise<void> {
    return request(`/api/v1/tasks/${id}`, { method: 'DELETE' })
}


