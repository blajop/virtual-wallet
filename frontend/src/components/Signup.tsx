import AlertTitle from "@mui/lab/AlertTitle";
import Alert from "@mui/material/Alert";
import Collapse from "@mui/material/Collapse";
import TextField from "@mui/material/TextField";
import { FormEvent, useEffect, useState } from "react";

interface Props {
  alertUsername: boolean;
  alertMsgUsername: string;
  alertEmail: boolean;
  alertMsgEmail: string;
  alertPhone: boolean;
  alertMsgPhone: string;
  alertPwd: boolean;
  alertMsgPwd: string;
}

export default function SignupForm(props: Props) {
  const alertUsername = props.alertUsername;
  const alertMsgUsername = props.alertMsgUsername;

  const alertEmail = props.alertEmail;
  const alertMsgEmail = props.alertMsgEmail;

  const alertPhone = props.alertPhone;
  const alertMsgPhone = props.alertMsgPhone;

  const alertPwd = props.alertPwd;
  const alertMsgPwd = props.alertMsgPwd;

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

  // PASSWORD MATCH TEST
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
              label={alertEmail ? alertMsgEmail : "Email"}
              name="email"
              autoComplete="email"
              error={alertEmail}
              onChange={handleInput}
            />
            <TextField
              required
              label={alertPhone ? alertMsgPhone : "Phone number"}
              name="phone"
              autoComplete="phone"
              error={alertPhone}
              onChange={handleInput}
            />
          </div>

          <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] flex flex-col">
            <TextField
              required
              label={alertUsername ? alertMsgUsername : "Username"}
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
              error={alertPwd}
              autoComplete="new-password"
              onChange={handleInput}
            />
            <Collapse in={alertPwd}>
              <Alert severity="error">{alertMsgPwd}</Alert>
            </Collapse>

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
