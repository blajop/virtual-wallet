import Box from "@mui/material/Box";
import { useEffect, useState } from "react";
import SelectSmall from "../Select/Select.tsx";
import { Wallet } from "../../pages/Profile.tsx";
import LabelCheckbox from "../Icons/CheckboxRecurr.tsx";
import SelectMisc from "../Select/SelectMisc.tsx";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import axios from "axios";
import { apiUrl } from "../../shared.ts";
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
  const [friendDefWallet, setFriendDefWallet] = useState("");
  const [loggedUsername, setLoggedUsername] = useState("");
  const friend = props.friend;

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
  const [currency, setCurrency] = useState("BGN");
  const selectCurrency = (value: string) => {
    setCurrency(value);
    return value;
  };

  // AMOUNT
  const [amount, setAmount] = useState("");
  const [focusAmount, setFocusAmount] = useState(false);
  const [alertAmount, setAlertAmount] = useState(false);
  useEffect(() => {}, [amount, wallet]);

  const checkAmount = () => {
    setFocusAmount(false);
    if (amount != "") {
      try {
        const parsed = parseFloat(amount);
        if (parsed <= 0) {
          setAlertAmount(true);
          return;
        }
      } catch (err) {
        setAlertAmount(true);
        return;
      }

      const url =
        apiUrl +
        `transactions/confirm_balance?wallet_id=${
          wallet!.id
        }&amount=${amount}&currency=${currency}`;
      axios
        .get(url, {
          headers: { Authorization: `Bearer ${localStorage.token}` },
        })
        .then((response) => {
          if (response.status === 200) {
            setAlertAmount(false);
            console.log(response);
          }
        })
        .catch(() => setAlertAmount(true));
    }
  };

  useEffect(() => {
    checkAmount();
  }, [wallet, currency]);

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
      <hr className="mt-[20px]"></hr>
      <Box sx={{ marginTop: "10px" }}>
        <SelectSmall username={loggedUsername} setWallet={handleSelectWallet} />

        <Box
          sx={{
            display: "flex",
            gap: "10px",
            marginBottom: "10px",
            marginTop: "30px",
          }}
        >
          <TextField
            required
            sx={{ width: "100%", flex: 2 }}
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
            onBlur={checkAmount}
            error={alertAmount}
            onChange={(e) => {
              setAmount(e.target.value);
            }}
          />
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
            sx={{ flex: 1 }}
          ></SelectMisc>
        </Box>
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
            sx={{ width: "100%", marginBottom: "10px" }}
            selectable={[recurrence, selectRecurrence]}
            options={["Monthly", "Annually"]}
            label="Recurrence"
          ></SelectMisc>
        )}
      </Box>
      <ButtonBlack
        invert={canConfirm ? true : false}
        sx={{ marginTop: "20px" }}
        onClick={handleConfirm}
        size="medium"
        disabled={!canConfirm}
        text={"Confirm Transaction"}
        disabledText="Please fill in the form"
      ></ButtonBlack>
      {successfulBanner ? (
        <Typography>Successful transaction!</Typography>
      ) : null}
    </>
  );
}
