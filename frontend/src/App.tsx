import React, { createContext, useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Welcome from "./pages/Welcome";
import Profile from "./pages/Profile";

export const LoginContext = createContext();

function App() {
  const [loggedIn, setLoggedIn] = useState(localStorage.token ? true : false);
  const [firstTimeVisit, setFirstTimeVisit] = useState(true);

  useEffect(() => {
    const visitedBefore = localStorage.getItem("visitedBefore");
    if (visitedBefore) {
      setFirstTimeVisit(false);
    } else {
      setFirstTimeVisit(true);
      setTimeout(() => {
        localStorage.setItem("visitedBefore", "true");
      }, 2000);
    }
  }, []);

  return (
    <LoginContext.Provider value={[loggedIn, setLoggedIn]}>
      <BrowserRouter>
        {firstTimeVisit && <Welcome />}
        <Header>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Header>
      </BrowserRouter>
    </LoginContext.Provider>
  );
}

export default App;
