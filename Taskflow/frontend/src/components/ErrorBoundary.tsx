

import { Component, type ErrorInfo, type ReactNode } from "react";


interface Props {
    children: ReactNode;
}


interface State {
    hasError: boolean;
}


export class ErrorBoundary extends Component<Props, State> {
    state: State = { hasError: false };

    static getDerivedStateFromError(): State {
        return {hasError: true};
    }

    componentDidCatch(error: Error) {
        console.error('Uncaught render error:', error);
    }

    render(): ReactNode {
        if (this.state.hasError) {
            return (
                <div className="">
                    <div className="text-center">
                        <p className="text-xl text-gray-800 mb-2">
                            Something went wrong.
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="text-blue-600 hover:underline"
                        >
                            Reload the page
                        </button>
                    </div>
                </div>
            )
        }
        return this.props.children;
    }

}




