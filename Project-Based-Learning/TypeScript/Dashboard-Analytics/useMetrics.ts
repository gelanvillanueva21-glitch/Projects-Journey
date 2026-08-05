

import { useState, useEffect } from "react";
import type { Metric, Period } from "./types";


interface UseMetricResult {
    data: Metric[] | null;
    isLoading: boolean;
    error: string | null;
}


const MOCK_DATA: Record<Period, Metric[]> = {
    "7d": [
        { label: "Total Revenue", current: 125000, previous: 100000, format: "currency" },
        { label: "Active Users", current: 8420, previous: 8000, format: "number" }
    ],
    "30d": [
        { label: "Total Revenue", current: 450000, previous: 380000, format: "currency" },
        { label: "Active Users", current: 12000, previous: 11500, format: "number" }
    ],
    "90d": [
        { label: "Total Revenue", current: 1200000, previous: 950000, format: "currency" },
        { label: "Active Users", current: 25000, previous: 20000, format: "number" },
    ]
}


export function useMetrics(period: Period): UseMetricResult {
    const [data, setData] = useState<Metric[] | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        setIsLoading(true);
        setError(null)

        const timer = setTimeout(() => {
            if (Math.random() < 0.1) {
                setError("Failed to load metrics. Please try again.");
                setData(null);
            } else
                setData(MOCK_DATA[period]);
            setIsLoading(false);
        }, 800);

        return () => clearTimeout(timer);
    }, [period]);

    return { data, isLoading, error}
}



