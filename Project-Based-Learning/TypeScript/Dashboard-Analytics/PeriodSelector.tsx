

import React from "react";
import type { Period } from "./types";


interface PeriodSelectorProps {
    selected: Period;
    onSelect: (period: Period) => void;
}


const PERIODS: Period[] = ["7d", "30d", "90d"]


export function PeriodSelector({ selected, onSelect }: PeriodSelectorProps): React.JSX.Element {
    return (
        <div className="period-selector">
            {PERIODS.map((period) => (
                <button
                    key={period}
                    className={period === selected ? "active" : ""}
                    onClick={() => onSelect(period)}
                >
                    {period}
                </button>
            ))}
        </div>
    );
}



