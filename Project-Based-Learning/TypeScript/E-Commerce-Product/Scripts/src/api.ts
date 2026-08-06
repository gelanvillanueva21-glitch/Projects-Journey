

import type { Product } from "./types";


const API_BASE = "https://fakestoreapi.com";


export async function fetchProducts(): Promise<Product[]> {
    const response = await fetch(`${API_BASE}/products`);
    if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}


export async function fetchProductById(id: number): Promise<Product> {
    const response = await fetch(`${API_BASE}/products/${id}`);
    if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}



