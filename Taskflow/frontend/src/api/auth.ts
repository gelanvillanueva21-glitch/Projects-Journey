
import { request } from "./client";
import type { LoginPayload, RegisterPayload, User } from "../types";


export function login(data: LoginPayload): Promise<{ message: string }> {
    return request('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify(data)
    })
}


export function register(data: RegisterPayload): Promise<User> {
    return request('/api/v1/auth/register', {
        method: 'POST',
        body: JSON.stringify(data)
    })
}


export function logout(): Promise<{ message: string }> {
    return request('/api/v1/auth/logout', { method: 'POST' })
}


export function getCurrentUser(): Promise<User> {
    return request('/api/v1/auth/me')
}


