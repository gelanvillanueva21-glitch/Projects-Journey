

import React from "react";

interface Product {
    id: number;
    name: string;
    price: number;
    inStock: boolean;
}


function ProductCard( props: {product: Product }): React.JSX.Element {
    return (
        <div className="product-card">
            <h2>{props.product.name}</h2>
            <p>${props.product.price.toFixed(2)}</p>
            <span>{props.product.inStock ? "In Stock" : "Out of Stock"}</span>
        </div>
    );
}


export default ProductCard;


