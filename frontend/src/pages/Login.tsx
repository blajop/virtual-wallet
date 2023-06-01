import { Snackbar } from "@mui/material";
import Box from "@mui/material/Box/Box";
import Container from "@mui/material/Container/Container";
import TextField from "@mui/material/TextField/TextField";
import { baseUrl } from "../shared.js";
import axios from "axios";
import { useState, useContext } from "react";
import { LoginContext } from "../App.js";
import { useNavigate } from "react-router-dom";
import LoadingButton from "@mui/lab/LoadingButton";

export default function Login() {
  const [, setLoggedIn] = useContext(LoginContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const navigate = useNavigate();
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  const login = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
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
            baseUrl + `static/avatars/${response.data.user_id}.png`
          );

          localStorage.setItem("token", response.data.access_token);
          navigate("/");
        }
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      })
      .finally(() => {});
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
        <Snackbar
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
          open={error}
          onClose={() => setError(false)}
          message="Invalid username or password!"
          key={"bottom" + "center"}
          ContentProps={{
            sx: {
              display: "flex",
              color: "white",
              fontWeight: "700",
              justifyContent: "center",
              backgroundColor: "black",
            },
          }}
        />
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
            id="username"
            onFocus={() => setError(false)}
            label="Username"
            autoComplete="username"
            error={error}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            id="password"
            type="password"
            label="Password"
            onFocus={() => setError(false)}
            error={error}
            autoComplete="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <LoadingButton
            variant="outlined"
            loading={loading}
            disabled={loading}
            type="submit"
            sx={{
              mt: "1rem",
              color: "white",
              backgroundColor: `${!loading ? "black" : "white"}`,
              textTransform: "none",
              borderColor: "black",
              "&:hover": {
                backgroundColor: "white",
                color: "black",
                borderColor: "black",
              },
            }}
          >
            <span>
              <strong>Log in</strong>
            </span>
          </LoadingButton>

          <Box className="flex flex-col mt-2">
            <a
              onClick={() => navigate("/")}
              className="text-blue-700 cursor-pointer"
            >
              Forgot password?
            </a>
            <a
              onClick={() => navigate("/")}
              className="text-blue-700 cursor-pointer"
            >
              Don't have an account yet?
            </a>
          </Box>
        </Box>
      </Container>
    </>
  );
}
