

export interface Metric {
    label: string;
    current: number;
    previous: number;
    format: "currency" | "percentage" | "number";
}


export interface Transaction {
    id: string;
    customer: string;
    amount: number;
    status: "completed" | "pending" | "failed";
    date: string;
}


export type Period = "7d" | "30d" | "90d";

