

import React, { useState } from "react";


function LoginForm(): React.JSX.Element {

    const [formData, setFormData] = useState({ email: "", password: ""})

    function handleChange(event: React.ChangeEvent<HTMLInputElement>): void {
        setFormData((prev) => ({
            ...prev,
            [event.target.name]: event.target.value
        }))
    }
    function handleSubmit(event: React.FormEvent<HTMLFormElement>): void {
        event.preventDefault()
        console.log(formData);
    }

    return (
        <form onSubmit={handleSubmit}>
            <input 
            type="email" 
            name="email" 
            value={formData.email} 
            onChange={handleChange} />
            <input 
            type="password" 
            name="password" 
            value={formData.password} 
            onChange={handleChange} />
            <button type="submit">Login</button>
        </form>
    );

}


export default LoginForm;


