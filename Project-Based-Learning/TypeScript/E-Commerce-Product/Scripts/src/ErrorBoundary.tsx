

import React, { Component, type ReactNode} from "react";


interface Props {
    children: ReactNode;
    fallback?: ReactNode;
}


interface State {
    hasError: boolean;
    error?: Error;
}


export class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false }
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error }
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
        console.log("ErrorBoundary caught an error:", error, errorInfo);
    }

    render(): ReactNode {
        if (this.state.hasError) {
            return (
                this.props.fallback ?? (
                    <div className="error-boundary">
                        <h2>Something went wrong.</h2>
                        <p>We're working on fixing it. Please try again later.</p>
                        {import.meta.env.DEV && (
                            <pre>{this.state.error?.message}</pre>
                        )}
                    </div>
                )
            );
        }
        return this.props.children;
    }
}




