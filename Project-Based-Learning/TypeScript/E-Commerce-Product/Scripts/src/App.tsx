

import React, { useState, useMemo, useCallback } from "react";
import { useQuery } from "@tanstack/react-query";
import { ProductGrid } from "./ProductGrid";
import { useCart } from "./CartContext";
import { ErrorBoundary } from "./ErrorBoundary";
import { fetchProducts } from "./api";
import type { Product } from "./types";


function App(): React.JSX.Element {
    const { addItem, totalItems } = useCart();
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedCategory, setSelectedCategory] = useState<string>("all");

    const { data: products, isLoading, error } = useQuery({
        queryKey: ["products"],
        queryFn: fetchProducts,
    })

    const categories = useMemo(() => {
        console.log("Category");
        if (!products)
            return ["all"];
        const cats = new Set(products.map((p) => p.category));
        return ["all", ...Array.from(cats)]
    }, [products]);

    const filteredProducts = useMemo(() => {
        if (!products)
            return []
        return products.filter((product) => {
            const matchesSearch = product.title
                .toLowerCase()
                .includes(searchQuery.toLowerCase());
            const matchesCategory = 
                selectedCategory === "all" || product.category === selectedCategory;
            return matchesSearch && matchesCategory;
        })  
    }, [products, searchQuery, selectedCategory]);
    
    console.log(`[Filtered Products]: [${filteredProducts}]`);
    const handleAddToCart = useCallback((product: Product): void => {
        console.log("Added:", product.title);
        addItem(product);
    }, [addItem])

    if (isLoading)
        return <div className="store"><p>Loading products...</p></div>
    if (error)
        return <div className="store">
            <p className="error">Failed to load products: {error.message}</p>
        </div>;

    console.log("[App]");
    return (
        <div className="store">
            <header className="store-header">
                <h1>Drift Store</h1>
                <span className="cart-badge">Cart: {totalItems}</span>
            </header>

            <div className="filters">
                <input 
                    type="text"
                    placeholder="Search products..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="search-input"
                />
                <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="category-select"
                >
                    {categories.map((cat) => (
                        <option key={cat} value={cat}>
                            {cat.charAt(0).toUpperCase() + cat.slice(1)}
                        </option>
                    ))}
                </select>
            </div>
            <ErrorBoundary>
                <ProductGrid products={filteredProducts} onAddToCart={handleAddToCart}/>
            </ErrorBoundary>
        </div>
    )

}


export default App;

