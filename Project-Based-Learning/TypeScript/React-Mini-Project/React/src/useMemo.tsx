

import { useMemo, useState } from "react";


function UseMemo(): React.JSX.Element {

    const [count, setCount] = useState(0);
    const [number, setNumber] = useState(0);

    const doubled = useMemo(() => {
        console.log("Calculating... ",number);
        return number + 2;
    }, [number]);

    return (
        <div>
            <h1>{doubled}</h1>
            <button onClick={() => setCount(count + 1)}>
                Increament Count {count}
            </button>
            <button onClick={() => setCount(count - 2)}>
                Decreament Count {count}
            </button>
            <button onClick={() => setNumber(number + 1)}>
                Increament Number
            </button>
        </div>
    )

}




export default UseMemo;




