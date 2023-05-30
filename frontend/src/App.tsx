import Header from "./components/Header";
import Home from "./pages/Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import { createContext, useState } from "react";

export const LoginContext = createContext();

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  return (
    <LoginContext.Provider value={[loggedIn, setLoggedIn]}>
      <BrowserRouter>
        <Header>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </Header>
      </BrowserRouter>
    </LoginContext.Provider>
  );
}

export default App;
