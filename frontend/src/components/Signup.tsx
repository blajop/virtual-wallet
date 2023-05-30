import TextField from "@mui/material/TextField";
import { FormEvent, useEffect, useState } from "react";

interface Props {
  alertUsername: boolean;
  alertEmail: boolean;
  alertPhone: boolean;
}

export default function Register(props: Props) {
  const alertUsername = props.alertUsername;
  const alertEmail = props.alertEmail;
  const alertPhone = props.alertPhone;
  const [alertConfirmPass, setalertConfirmPass] = useState(false);
  const [confirmPass, setConfirmPass] = useState("");

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

  const handleConfirmPass = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPass(event.target.value);
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
  };

  useEffect(() => {
    if (
      confirmPass != "" &&
      formReg["password"] != "" &&
      confirmPass != formReg["password"]
    ) {
      setalertConfirmPass(true);
    } else {
      setalertConfirmPass(false);
    }
  }, [confirmPass, formReg["password"]]);

  return {
    formReg,
    alertConfirmPass,
    confirmPass,
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
              label={
                alertConfirmPass ? "Passwords do not match" : "Confirm password"
              }
              type="password"
              name="password-confirm"
              error={alertConfirmPass}
              autoComplete="new-password"
              onChange={handleConfirmPass}
            />
          </div>
        </form>
      </>
    ),
  };
}
