

import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CartProvider } from "./CartContext";
import App from "./App";
import "./app_style.css"


const queryClient = new QueryClient();


ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <CartProvider>
                <App />
            </CartProvider>
        </QueryClientProvider>
    </React.StrictMode>
);


