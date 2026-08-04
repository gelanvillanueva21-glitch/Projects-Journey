

import React, { useState } from "react";
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


function App(): React.JSX.Element {
    const [period, setPeriod] = useState<Period>("7d")
    return (
        <div className="dashboard">
            <h1>Analytics Dashboard</h1>
            <PeriodSelector selected={period} onSelect={setPeriod}/>
            <div className="metrics-grid">
                {METRICS_DATA[period].map((metric) => (
                    <MetricCard key={metric.label} metric={metric}/>
                ))}
            </div>
        </div>
    );
}


export default App;


