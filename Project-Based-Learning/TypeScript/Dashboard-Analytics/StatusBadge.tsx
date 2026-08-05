

import React from "react"


type Status = "completed" | "pending" | "failed";


interface StatusBadgeProps {
    status: Status;
}


export function StatusBadge({ status }: StatusBadgeProps): React.JSX.Element {
    
    const classMap: Record<Status, string> = {
        completed: "badge-completed",
        pending: "badge-pending",
        failed: "badge-failed"
    };
    return <span className={`status-badge ${classMap[status]}`}>{status}</span>
}






