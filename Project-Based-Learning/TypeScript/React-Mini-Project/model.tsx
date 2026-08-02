

import React from "react"


interface ModalProps {
    title: string;
    children: React.ReactNode;
    isOpen?: boolean;
    onClose?: () => void;
}



function Modal({ title, children, isOpen = true, onClose }: ModalProps): React.JSX.Element | null {
    if (!isOpen) return null;
    return (
        <div className="modal-overlay">
            <div className="modal">
                <h2>{title}</h2>
                <div className="modal-body">
                    {children}
                    {onClose && <button onClick={onClose}>Close</button>}
                </div>
            </div>
        </div>
    );
}


export default Modal



