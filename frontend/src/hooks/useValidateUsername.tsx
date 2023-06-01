import { useEffect } from "react";
import axios from "axios";
import { baseUrl } from "../shared";

type Alert = [boolean, (e: boolean) => boolean];
type Msg = [string, (e: string) => string];

export default function useValidateUsername(
  username: string,
  alertState: Alert,
  msgState: Msg
) {
  const [, setAlertUsername] = alertState;
  const [, setAlertMsgUsername] = msgState;
  const USERNAME_REGEX = /^.{2,20}$/;

  useEffect(() => {
    if (username !== "") {
      if (!USERNAME_REGEX.test(username)) {
        setAlertUsername(true);
        setAlertMsgUsername("Username should be [2,20] chars long");
      } else {
        setAlertUsername(false);
        setAlertMsgUsername("");

        axios
          .get(`${baseUrl}api/v1/username-unique/${username}`)
          .then((response) => {
            if (response.status === 200) {
              setAlertUsername(false);
              setAlertMsgUsername("");
            }
          })
          .catch(() => {
            setAlertUsername(true);
            setAlertMsgUsername("Username is already taken");
          });
      }
    } else {
      setAlertUsername(false);
      setAlertMsgUsername("");
    }
  }, [username]);
}
