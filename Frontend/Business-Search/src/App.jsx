import Login from "./components/Login"
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Crawler from "./components/Crawler";


function App() {

  return (
    <div>      
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/operations" element={<Crawler/>} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
