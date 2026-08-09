

import React, { useState } from "react";


function IconTitle(): React.JSX.Element {

    return (
        <div className="title-icon">
            <button 
                onClick={() => window.location.reload()}
                className="task-icon">
                <img 
                    src="Icon/task_icon.svg" 
                    alt="Task Icon" />
            </button>
            <h2 className="title">Taskboard — Management</h2>
        </div>
    )

}


export default IconTitle;

