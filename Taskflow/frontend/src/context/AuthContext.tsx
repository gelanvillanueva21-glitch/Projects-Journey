

import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import type { User } from "../types";
import { getCurrentUser, login as apiLogin, logout as apiLogout } from "../api/auth";
import type { LoginPayload } from "../types";



interface AuthContextValue {
    user: User | null;
    isLoading: boolean;
    login: (data: LoginPayload) => Promise<void>;
    logout: () => Promise<void>;
}


const AuthContext = createContext<AuthContextValue | undefined>(undefined);


export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        getCurrentUser().then(setUser)
            .catch(() => setUser(null))
            .finally(() => setIsLoading(false))
    }, []);

    useEffect(() => {
        function handleUnauthorized() {
            setUser(null);
        }

        window.addEventListener('auth:unauthorized', handleUnauthorized);
        return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
    }, []);

    async function login(data: LoginPayload) {
        await apiLogin(data);
        const currentUser = await getCurrentUser();
        setUser(currentUser);
    }

    async function logout() {
        await apiLogout();
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, isLoading, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}



export function useAuth(): AuthContextValue {
    const context = useContext(AuthContext)

    if (context === undefined)
        throw new Error('useAuth must be used within an AuthProvider')
    return context;
}


