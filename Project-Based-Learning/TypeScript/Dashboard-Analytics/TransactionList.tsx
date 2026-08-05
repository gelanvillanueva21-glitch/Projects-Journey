

import React from "react";
import { StatusBadge } from "./StatusBadge";
import type { Transaction } from "./types";


interface TransactionListProps {
    transactions: Transaction[];
}


export function TransactionList({ transactions }: TransactionListProps): React.JSX.Element {
    if (transactions.length === 0)
        return <p>No transactions found.</p>;
    return (
        <div className="transaction-list">
            <h2>Recent Transactions</h2>
            <ul>
                {transactions.map((transaction) => (
                    <li key={transaction.id} className="transaction-item">
                        <span className="customer">{transaction.customer}</span>
                        <span className="amount">${transaction.amount.toFixed(2)}</span>
                        <span className="date">{transaction.date}</span>
                        <StatusBadge status={transaction.status}/>
                    </li>
                ))}
            </ul>
        </div>
    );
}




