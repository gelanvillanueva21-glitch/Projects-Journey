

import React  from "react";
import { useQuery } from "@tanstack/react-query";
import { ProductGrid } from "./ProductGrid";
import { useCart } from "./CartContext";
import { fetchProducts } from "./api";
import type { Product } from "./types";


function App(): React.JSX.Element {
    const { addItem, totalItems } = useCart();
    const { data: products, isLoading, error } = useQuery({
        queryKey: ["products"],
        queryFn: fetchProducts,
    })

    function handleAddToCart(product: Product): void {
        console.log("Added:", product.title);
        addItem(product);
    }

    if (isLoading)
        return <div className="store"><p>Loading products...</p></div>
    if (error)
        return <div className="store">
            <p className="error">Failed to load products: {error.message}</p>
        </div>;

    return (
        <div className="store">
            <header className="store-header">
                <h1>Drift Store</h1>
                <span className="cart-badge">Cart: {totalItems}</span>
            </header>
            <ProductGrid products={products ?? []} onAddToCart={handleAddToCart}/>
        </div>
    )

}


export default App;

