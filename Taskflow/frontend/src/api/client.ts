

const VITE_API_URL = import.meta.env.VITE_API_URL as string


class ApiError extends Error {
    status: number;
    constructor(status: number, message: string) {
        super(message);
        this.status = status;
    }
}


async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${VITE_API_URL}${path}`, {
        ...options,
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        }
    });

    if (response.status === 401) 
        window.dispatchEvent(new CustomEvent('auth:unauthorized'))

    if (!response.ok) {
        const body = await response.json().catch(() => ({
            detail: 'Unknown error'
        }));
        throw new ApiError(response.status, body.detail ?? 'Request Failed');
    }

    if (response.status === 204)
        return undefined as T;

    return response.json() as Promise<T>;
}


export { request, ApiError };


