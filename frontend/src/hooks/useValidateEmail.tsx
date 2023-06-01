import { useEffect } from "react";
import axios from "axios";
import { baseUrl } from "../shared";

type Alert = [boolean, (e: boolean) => boolean];
type Msg = [string, (e: string) => string];

export default function useValidateEmail(
  email: string,
  alertState: Alert,
  msgState: Msg
) {
  const [, setAlertEmail] = alertState;
  const [, setAlertMsgEmail] = msgState;
  const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  useEffect(() => {
    if (email != "") {
      if (!EMAIL_REGEX.test(email)) {
        setAlertEmail(true);
        setAlertMsgEmail("You should enter email input");
      } else {
        setAlertEmail(false);
        setAlertMsgEmail("");

        axios
          .get(`${baseUrl}api/v1/email-unique/${email}`)
          .then((response) => {
            if (response.status === 200) {
              setAlertEmail(false);
              setAlertMsgEmail("");
            }
          })
          .catch(() => {
            setAlertEmail(true);
            setAlertMsgEmail("Email is already taken");
          });
      }
    } else {
      setAlertEmail(false);
      setAlertMsgEmail("");
    }
  }, [email]);
}
