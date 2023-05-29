import Button from "@mui/base/Button";
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import Collapse from "@mui/material/Collapse";
import TextField from "@mui/material/TextField";
import { Fragment, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
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
    <Fragment>
      <form
        id="form"
        className="flex justify-center mt-20"
        onSubmit={handleSubmit}
      >
        <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] bg-blue-50 flex flex-col">
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
        </div>

        <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] bg-blue-50 flex flex-col">
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
        </div>
        <div className="mt-20">
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
      </form>
    </Fragment>
  );
}
