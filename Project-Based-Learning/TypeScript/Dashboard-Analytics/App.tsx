

import React, { useState } from "react";
import { MetricCard } from "./MetricCard";
import { PeriodSelector } from "./PeriodSelector";
import { TransactionList } from "./TransactionList";
import { useMetrics } from "./useMetrics";
import type { Metric, Period, Transaction } from "./types";


const TRANSACTIONS: Transaction[] = [
    { id: "txn-001", customer: "Acme Corp", amount: 12500, status: "completed", date: "2026-08-01" },
    { id: "txn-002", customer: "Globex", amount: 8300, status: "pending", date: "2026-08-02" },
    { id: "txn-003", customer: "Initech", amount: 4500, status: "failed", date: "2026-08-02" },
    { id: "txn-004", customer: "Umbrella", amount: 22000, status: "completed", date: "2026-08-02" },
    { id: "txn-005", customer: "AI", amount: 2500, status: "failed", date: "2026-08-14" },
    { id: "txn-006", customer: "Marvel", amount: 290000, status: "completed", date: "2026-08-31" },
]



function App(): React.JSX.Element {
    const [period, setPeriod] = useState<Period>("7d")
    const { data, isLoading, error } = useMetrics(period);

    return (
        <div className="dashboard">
            <h1>Analytics Dashboard</h1>
            <PeriodSelector selected={period} onSelect={setPeriod} />

            {isLoading && <p>Loading metrics...</p>}
            {error && <p className="error">{error}</p>}
            {data && (
                <div className="metrics-grid">
                    {data.map((metric) => (
                        <MetricCard key={metric.label} metric={metric} />
                    ))}
                </div>
            )}

            <TransactionList transactions={TRANSACTIONS} />
        </div>
    );
}


export default App;


