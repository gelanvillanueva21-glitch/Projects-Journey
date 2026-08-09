

import { useEffect, useState } from "react";


function Useeffect() {
    const [count, setCount] = useState(0)

    useEffect(() => {
        console.log("Count Changed!");
    }, [count]);

    return (
        <div>
            <h1>Count: {count}</h1>
            <button onClick={() => setCount(count + 1)}>
                Icrease
            </button>
        </div>
    )
}


export default Useeffect;




