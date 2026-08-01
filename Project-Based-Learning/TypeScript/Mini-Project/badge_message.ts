

type RequestState =
    | { kind: "idle" }
    | { kind: "loading"; progress: number }
    | { kind: "success"; data: string}
    | { kind: "error"; error: string}




function getBadgeMessage(state: RequestState): string {

    switch (state.kind) {
        case "idle":
            return "Idle";
        
        case "loading":
            return `Loading: ${state.progress}%`;
        
        case "success":
            return `Data Received: ${state.data}`;
        
        case "error":
            return `Error: ${state.error}`
        
        default:
            const _exhaustiveCheck: never = state;
            return _exhaustiveCheck;
    }

}



const idleState: RequestState = { kind: "idle" };
const loadingState: RequestState = { kind: "loading", progress : 50};
const successState: RequestState = { kind: "success", data : "I am John Cena, 16 Year old"};
const errorState: RequestState = { kind: "error", error : "Out of internet connection, please try again"}



console.log(getBadgeMessage(idleState));
console.log(getBadgeMessage(loadingState));
console.log(getBadgeMessage(successState));
console.log(getBadgeMessage(errorState));



// If i try to access idleState.progress Ide will give me an error because idleState in type RequestState
// does not have a progress value that made
// Ide giving : Property 'progress' doe not exist on type {kind : "idle"}.


