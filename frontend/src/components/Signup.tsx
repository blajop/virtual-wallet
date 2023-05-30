import TextField from "@mui/material/TextField";
import { Fragment, useState } from "react";
import axios from "axios";

interface Props {
  alertUsername: boolean;
  alertEmail: boolean;
  alertPhone: boolean;
}

export default function Register(props: Props) {
  const alertUsername = props.alertUsername;
  const alertEmail = props.alertEmail;
  const alertPhone = props.alertPhone;
  const [formReg, setFormReg] = useState({
    username: "",
    f_name: "",
    l_name: "",
    email: "",
    phone: "",
    password: "",
  });

  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormReg({ ...formReg, [event.target.name]: event.target.value });
  };

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    axios
      .post("http://localhost:8000/api/v1/signup", formReg)
      .then((response) => {
        if (response.status === 200) {
          setTimeout(() => {
            // navigate("/home");
          }, 3000);
        }
      })
      .catch((err) => console.log(err));
  }

  return {
    formReg,
    renderReg: (
      <>
        <form
          id="form"
          className="flex justify-center "
          onSubmit={handleSubmit}
        >
          <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] flex flex-col">
            <TextField
              required
              name="f_name"
              label="First name"
              autoComplete="none"
              onChange={handleInput}
            />
            <TextField
              required
              name="l_name"
              label="Last name"
              autoComplete="none"
              onChange={handleInput}
            />

            <TextField
              required
              label={alertEmail ? "Email is already taken" : "Email"}
              name="email"
              autoComplete="email"
              error={alertEmail}
              onChange={handleInput}
            />
            <TextField
              required
              label={
                alertPhone ? "Phone number is already taken" : "Phone number"
              }
              name="phone"
              autoComplete="phone"
              error={alertPhone}
              onChange={handleInput}
            />
          </div>

          <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] flex flex-col">
            <TextField
              required
              label={alertUsername ? "Username is already taken" : "Username"}
              name="username"
              error={alertUsername}
              onChange={handleInput}
              autoComplete="username"
            />

            <TextField
              required
              label="Password"
              type="password"
              name="password"
              autoComplete="new-password"
              onChange={handleInput}
            />

            <TextField
              required
              label="Confirm password"
              type="password"
              autoComplete="new-password"
            />
          </div>
        </form>
      </>
    ),
  };
}
