

import React, {useState, useCallback} from "react";


type ChildProps = {
    message: string;
    onClickHandle: () => void;
}


const Child = React.memo(({onClickHandle, message}: ChildProps) => {
    console.log("Child Rendered");
    return (
        <div>
            <h2>{message}</h2>
            <button onClick={onClickHandle}>Child Button</button>
        </div>
    )
})


function CallBack(): React.JSX.Element {
    const [firstNumber, setFirstNum] = useState(0);
    const [secondNumber, setSceondNum] = useState(0);

    const calculateNumber = useCallback(() => {
        if (firstNumber == 0 && secondNumber == 9)
            return <h1>Hello World!</h1>
        console.log("Calculating...");
        console.log(`[${firstNumber+secondNumber}]`);
        return firstNumber + secondNumber
    }, [firstNumber, secondNumber]);

    return (
        <div>
            <h1>Addition</h1>
            <input 
            type="number" 
            name="firstNumber" 
            onChange={(e) => setFirstNum(Number(e.target.value))}/>
            <input 
            type="number" 
            name="secondNumber"
            onChange={(e) => setSceondNum(Number(e.target.value))}/>
            <p>{calculateNumber()}</p>
            <button 
            onClick={calculateNumber}>
                Click To Calculcate
            </button>
        </div>
    )

}


export default CallBack


export function MemoCallBack() {
    const [count, setCount] = useState(0);

    const handleClick = () => {
        console.log("Children Clicked");
    }
    handleClick()
    console.log("Parent Renders");
    return (
        <div>
            <button onClick={() => setCount(count + 1)}>
                Count: ${count}
            </button>
            <Child 
            message="Greetings from Parent"
            onClickHandle={handleClick}/>
        </div>
    )
}




