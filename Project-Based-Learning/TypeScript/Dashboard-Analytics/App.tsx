

import React from "react";
import { MetricCard } from "./MetricCard.js";
import { PeriodSelector } from "./PeriodSelector.js";
import type { Metric, Period } from "./types.js";


const METRICS_DATA: Record<Period, Metric[]> = {
    "7d": [
        { label: "Total Revenue", current: 125000, previous: 100000, format: "currency" },
        { label: "Active Users", current: 8420, previous: 8000, format: "number" }
    ],
    "30d": [
        { label: "Total Revenue", current: 450000, previous: 380000, format: "currency" },
        { label: "Active Users", current: 12000, previous: 11500, format: "number"}
    ],
    "90d": [
        { label: "Total Revenue", current: 1200000, previous: 950000, format: "currency" },
        { label: "Active Users", current: 25000, previous: 20000, format: "number" }
    ]
};


const revenueData: Metric = {
    label: "Total Revenue",
    current: 125000,
    previous: 100000,
    format: "currency"
}


const usersData: Metric = {
    label: "Active Users",
    current: 8450,
    previous: 8000,
    format: "number"
}


function App(): React.JSX.Element {
    return (
        <div className="dashboard">
            <h1>Analytics Dashboard</h1>
            <div className="metrics-grid">
                <MetricCard metric={revenueData}/>
                <MetricCard metric={usersData}/>
            </div>
        </div>
    );
}


export default App;


