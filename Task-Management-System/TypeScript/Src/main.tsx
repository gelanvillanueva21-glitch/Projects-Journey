

import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App } from "./App";
import "./global_style.css";


// SIDE BAR STYLE
import "./side_bar/Css/side_bar.css";
import "./side_bar/Css/title_style.css";
import "./side_bar/Css/profile.css";
import "./side_bar/Css/change_password.css";
import "./side_bar/Css/buttons.css";
import "./side_bar/Css/login.css";
import "./side_bar/Css/logout.css";
import "./side_bar/Css/register.css";




const queryClient = new QueryClient();


ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <App/>
        </QueryClientProvider>
    </React.StrictMode>
)




