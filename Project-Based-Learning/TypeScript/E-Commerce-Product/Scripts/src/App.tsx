

import React, { useState }  from "react";
import { ProductGrid } from "./ProductGrid";
import type { Product } from "./types";



const SAMPLE_PRODUCTS: Product[] = [
    {
        id: 1,
        title: "Fjallraven Backpack",
        price: 109.95,
        description: "Your perfect pack for everyday use.",
        category: "men's clothing",
        image: "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
        rating: { rate: 3.9, count: 120 },
    },
    {
        id: 2,
        title: "Mens Casual Premium Slim Fit T-Shirts",
        price: 22.3,
        description: "Slim-fitting style.",
        category: "men's clothing",
        image: "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
        rating: { rate: 4.1, count: 259 },
    },
    {
        id: 3,
        title: "Mens Cotton Jacket",
        price: 55.99,
        description: "Great outerwear jackets for Spring/Autumn/Winter.",
        category: "men's clothing",
        image: "https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
        rating: { rate: 4.7, count: 500 },
    }
]


function App(): React.JSX.Element {
    const [cartCount, setCartCount] = useState(0);
    function handleAddToCart(product: Product): void {
        console.log("Added:", product.title);
        setCartCount((prev) => prev + 1)
    }

    return (
        <div className="store">
            <header className="store-header">
                <h1>Drift Store</h1>
                <span className="cart-badge">Cart: {cartCount}</span>
            </header>
            <ProductGrid products={SAMPLE_PRODUCTS} onAddToCart={handleAddToCart}/>
        </div>
    )

}


export default App;

