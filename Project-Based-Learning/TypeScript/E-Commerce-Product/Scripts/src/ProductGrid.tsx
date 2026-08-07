

import React from "react";
import { ProductCard } from "./ProductCard";
import type { Product } from "./types";



interface ProductGridProps {
    products: Product[];
    onAddToCart: (product: Product) => void;
}


export function ProductGrid({ products, onAddToCart }: ProductGridProps): React.JSX.Element {
    if (products.length === 0)
        return <p className="empty-grid">No products available.</p>;
    console.log(`[Product Grid]: [${products}]`);
    return (
        <div className="product-grid">
            {products.map((product) => (
                <ProductCard 
                key={product.id}
                product={product}
                onAddToCart={onAddToCart}
                />
            ))}
        </div>
    )
}





