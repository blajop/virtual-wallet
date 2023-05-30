import { Checkbox, Typography } from "@mui/material";
import Box from "@mui/material/Box/Box";
import Button from "@mui/material/Button/Button";
import Container from "@mui/material/Container/Container";
import TextField from "@mui/material/TextField/TextField";
import { baseUrl } from "../shared.js";
import axios from "axios";
import { useState, useContext } from "react";
import { LoginContext } from "../App.js";

export default function Login() {
  const [loggedIn, setLoggedIn] = useContext(LoginContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  const login = (e) => {
    e.preventDefault();
    const url = baseUrl + "api/v1/login/access-token";
    axios
      .post(url, data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
      .then((response) => {
        if (response.status === 200) {
          setLoggedIn(true);
          localStorage.setItem(
            "avatar",
            baseUrl + `static/avatars/${response.data.user_id}.jpg`
          );

          localStorage.setItem("token", response.data.access_token);
        }
      })
      .catch((err) => console.log(err));
  };
  return (
    <>
      <Container
        sx={{
          display: "flex",
          justifyContent: "center",
          height: "calc(100vh - 60px)",
        }}
      >
        <Box
          component="form"
          onSubmit={(e) => login(e)}
          className="flex flex-col justify-center gap-2"
          sx={{
            "& .MuiTextField-root": { m: 0, width: "25ch" },
          }}
          autoComplete="off"
        >
          <TextField
            size="small"
            id="username"
            label="Username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            size="small"
            id="password"
            type="password"
            label="Password"
            autoComplete="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            variant="outlined"
            size="small"
            type="submit"
            sx={{
              mt: "1rem",
              color: "white",
              backgroundColor: "black",
              textTransform: "none",
              "&:hover": {
                backgroundColor: "white",
                color: "black",
                borderColor: "black",
              },
            }}
          >
            <strong>Log in</strong>
          </Button>
        </Box>
      </Container>
    </>
  );
}
