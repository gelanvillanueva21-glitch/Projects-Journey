

interface User{name : string, age : Number}



function greetings(user : User) {
    return `Hello ${user.name.toUpperCase()}`;
}


let data : User = {
    name : "gelan",
    age : 12
}
const message = greetings(data)
console.log(message);







