

import React, { useState } from "react";



const Child = React.memo(({ greeting }: { greeting: string }) => {
    console.log("Child Rendered");
    return <h2>{greeting}</h2>
})


function App() {
    const [count, setCount] = useState(0);
    const [greetMsg, setGreetMsg] = useState("Hello");
    console.log("App Rendered");
    
    function ClickButton() {
        setCount(count + 1);
        setGreetMsg("Button Clicked!")
        console.log("Clicked");
    }



    return (
        <div>
            <input 
                type="text"
                placeholder="Hello!"
                onChange={(e) => setGreetMsg(e.target.value)}
            />
            <button 
                onClick={ClickButton}>
                Count: {count}
            </button>
            <Child greeting={greetMsg}/>
        </div>
    )
}


export default App


