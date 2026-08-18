

import { BrowserRouter, Routes, Route} from 'react-router-dom'
import LoginPage from "./pages/LoginPage";
import { DashBoard } from "./router/DashboardRoute";
import { ProtectedRoute } from "./router/ProtectedRoute";



function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='login' element={<LoginPage/>}/>
                <Route 
                    path='/' 
                    element={
                        <ProtectedRoute>
                            <DashBoard/>
                        </ProtectedRoute>
                    } />
            </Routes>
        </BrowserRouter>
    )
}


export default App;

