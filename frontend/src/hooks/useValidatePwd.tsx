import { useEffect } from "react";

type Alert = [boolean, (e: boolean) => boolean];
type Msg = [string, (e: string) => string];

export default function useValidatePwd(
  password: string,
  alertState: Alert,
  msgState: Msg
) {
  const [, setAlertPwd] = alertState;
  const [, setAlertMsgPwd] = msgState;
  const PWD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$/;

  useEffect(() => {
    if (password != "") {
      if (!PWD_REGEX.test(password)) {
        setAlertPwd(true);
        setAlertMsgPwd(
          "Password must be at least 8 characters  and contain at least one uppercase, lowercase, digit, symbol"
        );
      } else {
        setAlertPwd(false);
        setAlertMsgPwd("");
      }
    } else {
      setAlertPwd(false);
      setAlertMsgPwd("");
    }
  }, [password]);
}
