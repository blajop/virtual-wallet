import { useEffect } from "react";
import axios from "axios";
import { baseUrl } from "../shared";

type Alert = [boolean, (e: boolean) => boolean];
type Msg = [string, (e: string) => string];

export default function useValidatePhone(
  phone: string,
  alertState: Alert,
  msgState: Msg
) {
  const [, setAlertPhone] = alertState;
  const [, setAlertMsgPhone] = msgState;
  const PHONE_REGEX = /^\d{10}$/;

  useEffect(() => {
    if (phone != "") {
      if (!PHONE_REGEX.test(phone)) {
        setAlertPhone(true);
        setAlertMsgPhone("Phone should be valid 10 digits long");
      } else {
        setAlertPhone(false);
        setAlertMsgPhone("");

        setTimeout(() => {
          axios
            .get(`${baseUrl}api/v1/phone-unique/${phone}`)
            .then((response) => {
              console.log(response.data);
              if (response.status === 200) {
                setAlertPhone(false);
                setAlertMsgPhone("");
              }
            })
            .catch(() => {
              setAlertPhone(true);
              setAlertMsgPhone("Phone is already taken");
            });
        }, 500);
      }
    } else {
      setAlertPhone(false);
      setAlertMsgPhone("");
    }
  }, [phone]);
}
