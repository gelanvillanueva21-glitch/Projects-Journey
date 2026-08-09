

import { useEffect, useRef } from "react";




function UseRef() {
    
    let inputRef = useRef<HTMLInputElement>(undefined);
    let ref = useRef(0);
    useEffect(() => {
        console.log("Component Render!");
        console.log(inputRef);
    })

    function handleClick() {
        ref.current++;
        inputRef.current?.focus();
        if (inputRef.current) {
            inputRef.current.style.backgroundColor = "blue";
        }
        console.log(ref.current);
    }

    return (
        <div>
            <button onClick={handleClick}>
                Click me!
            </button>
            <input ref={inputRef} />
        </div>
    )

}


export default UseRef;


