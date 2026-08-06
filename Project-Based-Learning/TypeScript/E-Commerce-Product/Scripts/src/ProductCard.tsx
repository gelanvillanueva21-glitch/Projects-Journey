

import React from "react";
import type { Product } from "./types";


interface ProductCardProps {
    product: Product;
    onAddToCart: (product: Product) => void;
}


export function ProductCard({ product, onAddToCart }: ProductCardProps): React.JSX.Element {
    function handleAddToCart(): void {
        onAddToCart(product);
    }

    return (
        <div className="product-card">
            <img 
                src={product.image} 
                alt={product.title}
                className="product-image"
                onError={(e) => {
                    (e.target as HTMLImageElement).src = "https://via.placeholder.com/200";
                }}
            />
            <div className="product-info">
                <span className="product-category">{product.category}</span>
                <h3 className="product-title">{product.title}</h3>
                <div className="product-rating">
                    ⭐ {product.rating.rate} ({product.rating.count} reviews)
                </div>
                <p className="product-price">${product.price.toFixed(2)}</p>
                <button 
                    className="add-to-cart-btn" 
                    onClick={handleAddToCart}>
                    Add To Cart
                </button>
            </div>
        </div>
    )
}





