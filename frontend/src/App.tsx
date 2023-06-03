import React, { useState, useEffect, Dispatch, SetStateAction } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Register from "./pages/Register.tsx";
import Login from "./pages/Login";
import Welcome from "./pages/Welcome";
import Profile from "./pages/Profile";
import axios from "axios";
import { baseUrl } from "./shared.ts";
import FriendInvite from "./components/Modals/FriendInvite.tsx";

export const LoginContext = React.createContext<ILoginContext>([
  false,
  () => {},
]);
type ILoginContext = [boolean, React.Dispatch<React.SetStateAction<boolean>>];

type IAvatarContext = {
  updatedAvatar: string;
  setUpdatedAvatar: Dispatch<SetStateAction<string>>;
};

export const AvatarContext = React.createContext<IAvatarContext>({
  updatedAvatar: "",
  setUpdatedAvatar: () => {},
});

function App() {
  const [loggedIn, setLoggedIn] = useState(localStorage.token ? true : false);
  const [updatedAvatar, setUpdatedAvatar] = useState(localStorage.avatar ?? "");

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

  // Verify token
  useEffect(() => {
    if (localStorage.token) {
      axios
        .get(baseUrl + "api/v1/users/profile", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        })
        .catch((err) => {
          if (err.response.status === 403) {
            setLoggedIn(false);
            localStorage.removeItem("token");
          }
        });
    }
  }, []);

  return (
    <LoginContext.Provider value={[loggedIn, setLoggedIn]}>
      <AvatarContext.Provider value={{ updatedAvatar, setUpdatedAvatar }}>
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
      </AvatarContext.Provider>
    </LoginContext.Provider>
  );
}

export default App;
