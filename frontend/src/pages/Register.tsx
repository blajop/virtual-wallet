import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState, useEffect } from "react";
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import Collapse from "@mui/material/Collapse";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import CircularProgress from "@mui/material/CircularProgress";
import Container from "@mui/material/Container";
export default function Register() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 300);
  }, []);

  const [form, setForm] = useState({
    username: "",
    f_name: "",
    l_name: "",
    email: "",
    phone: "",
    password: "",
  });
  const [open, setOpen] = useState(false);
  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };
  const navigate = useNavigate();

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    axios
      .post("http://localhost:8000/api/v1/signup", form)
      .then((response) => {
        if (response.status === 200) {
          setOpen(true);
          setTimeout(() => {
            navigate("/home");
          }, 3000);
        }
      })
      .catch((err) => console.log(err));
  }

  return (
    <form
      id="form"
      className="flex justify-center mt-20"
      onSubmit={handleSubmit}
    >
      {loading ? (
        <div className="pt-40 flex items-center">
          <CircularProgress className="flex align-center" />
        </div>
      ) : (
        <div className="w-[800px] justify-center gap-[10px] rounded p-[40px] bg-blue-50 flex flex-col">
          <TextField
            required
            id="outlined-required"
            name="f_name"
            label="First name"
            autoComplete="none"
            onChange={handleInput}
          />
          <TextField
            required
            id="outlined-required"
            name="l_name"
            label="Last name"
            autoComplete="none"
            onChange={handleInput}
          />

          <TextField
            required
            id="outlined-required"
            label="Email"
            name="email"
            autoComplete="email"
            onChange={handleInput}
          />
          <TextField
            required
            id="outlined-required"
            label="Phone number"
            name="phone"
            autoComplete="phone"
            onChange={handleInput}
          />

          <TextField
            required
            id="outlined-required"
            label="Username"
            name="username"
            onChange={handleInput}
          />

          <TextField
            required
            id="outlined-password-input"
            label="Password"
            type="password"
            name="password"
            autoComplete="new-password"
            onChange={handleInput}
          />

          <TextField
            required
            id="outlined-password-input"
            label="Confirm password"
            type="password"
            autoComplete="new-password"
          />
          <Button
            sx={{ fontWeight: "bold", fontSize: "1rem", mt: "20px" }}
            variant="contained"
            type="submit"
          >
            Register
          </Button>
          <Collapse in={open}>
            <Alert severity="success">
              <AlertTitle>
                <strong>Successful registration</strong>
              </AlertTitle>
              You will now be redirected to the homepage.
            </Alert>
          </Collapse>
        </div>
      )}
    </form>
  );
}
