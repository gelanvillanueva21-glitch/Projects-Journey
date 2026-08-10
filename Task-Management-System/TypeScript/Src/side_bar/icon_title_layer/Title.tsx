

import React from "react";
import icon from "./Icon/task_icon.svg"


function IconTitle(): React.JSX.Element {

    return (
        <div className="title-icon">
            <button 
                onClick={() => window.location.reload()}
                className="task-icon">
                <img 
                    src={icon} 
                    alt="Task Icon" />
            </button>
            <h2 className="title">Taskboard Management</h2>
        </div>
    )

}


export default IconTitle;

