import { useEffect } from "react";

type Flag = [boolean, (e: boolean) => boolean];

export default function useValidateCanSubmit(
  canSubmit: Flag,
  alertConfirmPass: boolean,
  alertUsername: boolean,
  alertEmail: boolean,
  alertPhone: boolean,
  f_name: string,
  l_name: string,
  username: string,
  email: string,
  phone: string,
  password: string,
  confirmPass: string
) {
  const [, setCanSubmit] = canSubmit;

  useEffect(() => {
    const conditions = [
      !alertConfirmPass,
      !alertUsername,
      !alertEmail,
      !alertPhone,
    ];
    const conditions2 = [
      f_name,
      l_name,
      username,
      email,
      phone,
      password,
      confirmPass,
    ];
    if (
      conditions.every((element) => element === true) &&
      conditions2.every((element) => element != "")
    ) {
      setCanSubmit(true);
    } else {
      setCanSubmit(false);
    }
  });
}
