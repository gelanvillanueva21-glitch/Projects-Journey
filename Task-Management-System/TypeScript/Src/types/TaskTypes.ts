

export interface Task {
    title: string;
    description: string;
    status: "todo" | "in-progress" | "set-aside" | "done";
    priority: "low" | "medium" | "high";
    createdAt: string;
    dueDate?: string;
}



