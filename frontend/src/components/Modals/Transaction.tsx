import Box from "@mui/material/Box";
import { useEffect, useState } from "react";
import SelectSmall from "../Select/Select.tsx";
import { Wallet } from "../../pages/Profile.tsx";
import LabelCheckbox from "../Icons/CheckboxRecurr.tsx";
import SelectMisc from "../Select/SelectMisc.tsx";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import axios from "axios";
import { apiUrl, baseUrl } from "../../shared.ts";
import TextField from "@mui/material/TextField";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";
import Typography from "@mui/material/Typography";

type dataState = [boolean, (e: boolean) => boolean];

interface Props {
  friend: Friend;
  transactionOpen: dataState;
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
  const [friendDefWallet, setFriendDefWallet] = useState("");
  const [loggedUsername, setLoggedUsername] = useState("");

  const [transactionOpen, setTransactionOpen] = props.transactionOpen;

  const [successfulBanner, setSuccessfulBanner] = useState(false);

  // GET LOGGED USER - UPON LOAD
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

  // GET RECEIVER DEFAULT WALLET
  useEffect(() => {
    const url = apiUrl + `users/${friend.id}/wallets/default`;
    axios
      .get(url, { headers: { Authorization: `Bearer ${localStorage.token}` } })
      .then((response) => {
        const walletId: string = response.data.id;
        setFriendDefWallet(walletId);
      })
      .catch((err) => console.log(err));
  }, []);

  // EMITTING WALLET
  const handleSelectWallet = (wallet: Wallet | undefined) => {
    setWallet(wallet);
  };

  // RECURRENCE
  const [recurringChecked, setRecurringChecked] = useState(false);
  const [recurrence, setRecurrence] = useState("");
  const selectRecurrence = (value: string) => {
    setRecurrence(value);
    return value;
  };
  useEffect(() => {
    if (recurringChecked === false) {
      setRecurrence("");
    }
  }, [recurringChecked]);

  // CURRENCY
  const [currency, setCurrency] = useState("");
  const selectCurrency = (value: string) => {
    setCurrency(value);
    return value;
  };

  // AMOUNT
  const [amount, setAmount] = useState("");
  const [focusAmount, setFocusAmount] = useState(false);
  const [alertAmount, setAlertAmount] = useState(false);
  useEffect(() => {
    if (amount != "") {
      try {
        if (parseFloat(amount) <= 0 || wallet!.balance < parseFloat(amount)) {
          setAlertAmount(true);
        } else {
          setAlertAmount(false);
        }
      } catch (err) {
        setAlertAmount(true);
      }
    } else {
      setAlertAmount(false);
    }
  }, [amount, wallet]);

  // DETAIL
  const [detail, setDetail] = useState("");

  // CONDITIONS

  const [canConfirm, setCanConfirm] = useState(false);

  useEffect(() => {
    const conditions = [currency, amount, detail];

    if (conditions.every((element) => element != "") && alertAmount === false) {
      setCanConfirm(true);
    } else {
      setCanConfirm(false);
    }
  }, [currency, amount, detail, alertAmount]);

  // CONFIRM AND CREATE THE TRANSACTION
  const handleConfirm = () => {
    const finalData = {
      wallet_sender: wallet!.id,
      card_sender: null,
      receiving_user: friend.id,
      wallet_receiver: friendDefWallet,
      currency: currency,
      amount: amount,
      recurring: recurrence != "" ? recurrence : null,
      detail: detail,
    };
    axios
      .post(`${apiUrl}transactions`, finalData, {
        headers: {
          Authorization: `Bearer ${localStorage.token}`,
        },
      })
      .then((response) => {
        if (response.status === 201) {
          console.log(response);
          setSuccessfulBanner(true);
          setTimeout(() => {
            setSuccessfulBanner(false);
            setTransactionOpen(false);
          }, 3000);
        }
      })
      .catch();
  };

  return (
    <>
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
        <SelectMisc
          selectable={[currency, selectCurrency]}
          options={[
            "USD",
            "EUR",
            "BGN",
            "CAD",
            "AUD",
            "CHF",
            "CNY",
            "JPY",
            "GBP",
            "NOK",
          ]}
          label="Currency"
        ></SelectMisc>
        <TextField
          required
          sx={{ width: "100%" }}
          label={"Amount"}
          name="amount"
          value={
            focusAmount
              ? amount
              : amount === ""
              ? ""
              : parseFloat(amount).toFixed(2)
          }
          onFocus={() => setFocusAmount(true)}
          onBlur={() => setFocusAmount(false)}
          error={alertAmount}
          onChange={(e) => {
            setAmount(e.target.value);
          }}
        />
        <TextField
          required
          sx={{ width: "100%" }}
          label={"Detail"}
          name="detail"
          value={detail}
          onChange={(e) => {
            setDetail(e.target.value);
          }}
        />
      </Box>
      <ButtonBlack
        invert={canConfirm ? true : false}
        onClick={handleConfirm}
        size="medium"
        disabled={!canConfirm}
        text={"Confirm Transaction"}
        disabledText="Please fill in the data"
      ></ButtonBlack>
      {successfulBanner ? (
        <Typography>Successful transaction!</Typography>
      ) : null}
    </>
  );
}
