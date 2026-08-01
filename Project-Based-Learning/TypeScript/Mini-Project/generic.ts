


type ApiResponse<T> =
    | {status: "loading"}
    | {status: "success", data: T}
    | {status: "error", error: string}



function formatResponse<T>(response: ApiResponse<T>): string {

    switch (response.status) {
        case "loading":
            return "Loading..."
        
        case "success":
            const formatedData = typeof response.data === "object"
                ? JSON.stringify(response.data)
                :response.data
            return `Success: ${formatedData}`;
        
        case "error":
            return `Error: ${response.error}`;
        
        default:
            const _exhaustiveCheck: never = response;
            return _exhaustiveCheck;
    }


}


interface User { id: number; name: string };


interface Product { sku: string; price: number };


const productData: ApiResponse<Product> = { status: "success", data: { sku: "jk141dabW141", price: 120 } };
const userData: ApiResponse<User> = { status: "success", data: { id: 120412, name: "John Cena" }};


console.log(formatResponse<User>({ status: "loading"}));
console.log(formatResponse(productData));
console.log(formatResponse<Product>({ status: "error", error: "Internet  connection cut off"}));
console.log(formatResponse(userData));







