
import React from "react";
import type {Metric} from "./types";


interface MetricCardProps {
    metric: Metric;
}


export function MetricCard({ metric }: MetricCardProps): React.JSX.Element {
    const change = metric.previous === 0 ? 0 : ((metric.current - metric.previous) / metric.previous) * 100;
    const isPositive = change >= 0;

    function formatValue(value: number, format: Metric["format"]): string {
        switch (format) {
            case "currency":
                return `$${value.toLocaleString()}`;
            case "percentage":
                return `${value.toFixed(1)}%`;
            case "number":
                return value.toLocaleString();
            default:
                const _exhaustiveCheck: never = format;
                return _exhaustiveCheck;
        }
    }
    
    return (
        <div className="metric-card">
            <h3>{metric.label}</h3>
            <p className="metric-value">
                {formatValue(metric.current, metric.format)}
            </p>
            <p className={isPositive ? "trend-positive" : "trend-negative"}>
                {isPositive ? "↑" : "↓"} {Math.abs(change).toFixed(1)}%
            </p>
        </div>
    );
}




