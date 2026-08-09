

import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import SideBarLayer from "./side_bar/SideBar";


const queryClient = new QueryClient();


ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <main>
                <SideBarLayer/>
            </main>
        </QueryClientProvider>
    </React.StrictMode>
)




