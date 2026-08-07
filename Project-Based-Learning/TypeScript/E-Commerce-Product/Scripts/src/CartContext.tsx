

import React, { createContext, useContext, useState, useCallback} from "react";
import type { Product, CartItem } from "./types";


interface CartContextType {
    items: CartItem[];
    addItem: (product: Product) => void;
    removeItem: (productId: number) => void;
    totalItems: number;
    totalPrice: number;
}


const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }): React.JSX.Element {
    const [items, setItems] = useState<CartItem[]>([]);

    const addItem = useCallback((product: Product): void => {
        setItems((prev) => {
            console.log("Item added!");
            const existing = prev.find((item) => item.product.id === product.id);
            if (existing) {
                return prev.map((item) => 
                    item.product.id === product.id
                    ? { ...item, quantity: item.quantity + 1}
                    : item
                );
            }
            return [...prev, { product, quantity: 1 }]
        })
    }, []);

    const removeItem = useCallback((productId: number): void => {
        setItems((prev) => prev.filter((item) => item.product.id !== productId));
    }, []);

    const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

    console.log("[Cart Context]");
    return (
        <CartContext.Provider value={{ items, addItem, removeItem, totalItems, totalPrice }}>
            {children}
        </CartContext.Provider>
    );
}


export function useCart(): CartContextType {
    const context = useContext(CartContext);
    if (context === undefined)
        throw new Error("useCart must be used within a CartProvider");
    console.log(`[Use Cart]: [${context}]`);
    return context;
}




