import Box from "@mui/material/Box";
import { useEffect, useState } from "react";
import SelectSmall from "../Select/Select.tsx";
import { Wallet } from "../../pages/Profile.tsx";
import LabelCheckbox from "../Icons/CheckboxRecurr.tsx";
import SelectMisc from "../Select/SelectMisc.tsx";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import axios from "axios";
import { apiUrl } from "../../shared.ts";

interface Props {
  friend: Friend;
}

export type User = {
  username: string;
  email: string;
  phone: string;
  f_name: string;
  l_name: string;
  id: string;
  password: string;
  user_settings: string;
};

export default function Transaction(props: Props) {
  const [wallet, setWallet] = useState<Wallet | undefined>();
  const friend = props.friend;
  const [loggedUsername, setLoggedUsername] = useState("");

  useEffect(() => {
    const url = apiUrl + `users/profile`;

    axios
      .get(url, { headers: { Authorization: `Bearer ${localStorage.token}` } })
      .then((response) => {
        const loggedUser: User = {
          username: response.data.username,
          email: response.data.email,
          phone: response.data.phone,
          f_name: response.data.f_name,
          l_name: response.data.l_name,
          id: response.data.id,
          password: response.data.password,
          user_settings: response.data.user_settings,
        };
        setLoggedUsername(loggedUser.username);
      })
      .catch((err) => console.log(err));
  }, []);

  // Transaction data
  const [recurringChecked, setRecurringChecked] = useState(false);
  const [recurrence, setRecurrence] = useState("");

  const handleSelectWallet = (wallet: Wallet | undefined) => {
    setWallet(wallet);
  };

  const selectRecurrence = (value: string) => {
    setRecurrence(value);
    return value;
  };

  useEffect(() => {
    if (recurringChecked === false) {
      setRecurrence("");
    }
  }, [recurringChecked]);

  //   const handleSend = () => {

  //     const finalData = {

  //     };
  //     axios
  //       .put(`${baseUrl}api/v1/users/profile`, finalData, {
  //         headers: {
  //           Authorization: `Bearer ${localStorage.getItem("token")}`,
  //         },
  //       })
  //       .then((response) => {
  //         if (response.status === 200) {
  //           console.log(response);
  //         }
  //       })
  //       .catch();
  //     handleClose();
  //   };

  return (
    <div>
      <Box>
        <SelectSmall username={loggedUsername} setWallet={handleSelectWallet} />
        <LabelCheckbox
          isChecked={[
            recurringChecked,
            (value: boolean) => {
              setRecurringChecked(value);
              return value;
            },
          ]}
        />
        {recurringChecked && (
          <SelectMisc
            selectable={[recurrence, selectRecurrence]}
            options={["month", "year"]}
            label="Recurrence"
          ></SelectMisc>
        )}
      </Box>
    </div>
  );
}
