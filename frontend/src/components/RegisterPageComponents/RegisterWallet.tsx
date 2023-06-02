import { useEffect, useState } from "react";
import WalletCard from "../Wallet/WalletCard";
import Box from "@mui/material/Box/Box";
import Select from "@mui/material/Select/Select";
import MenuItem from "@mui/material/MenuItem/MenuItem";
import TextField from "@mui/material/TextField/TextField";
import Paper from "@mui/material/Paper/Paper";
import axios from "axios";
import { apiUrl, baseUrl } from "../../shared";

const currencies = [
  `BGN`,
  `USD`,
  `EUR`,
  `GBP`,
  `CHF`,
  `CAD`,
  `AUD`,
  `CNY`,
  `JPY`,
  `NOK`,
];

export default function WalletCreate({
  username,
  password,
  setToken,
  setWalletName,
  setWalletCurr,
}: {
  username: string;
  password: string;
  setToken: (e: string) => void;
  setWalletName: (e: string) => void;
  setWalletCurr: (e: string) => void;
}) {
  const [name, setName] = useState("Wallet");
  const [currency, setCurrency] = useState("BGN");

  const url = apiUrl + "login/access-token";
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  // GET TOKEN
  useEffect(() => {
    axios
      .post(url, data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
      .then((response) => {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("avatar", baseUrl + `static/avatars/none.png`);
        setToken(response.data.access_token);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <>
      <Paper
        elevation={2}
        sx={{
          display: "flex",
          flexDirection: "column",
          width: `70%`,
          mt: "40px",
          padding: "20px",
          gap: `20px`,
        }}
      >
        <Box
          sx={{
            width: `100%`,
            display: "flex",
            justifyContent: "space-between",
            gap: "20px",
          }}
        >
          <TextField
            id="wallet-name"
            label="Wallet name"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setWalletName(name);
            }}
            sx={{ flex: 3 }}
          />
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={currency}
            defaultValue="BGN"
            label={"Currency"}
            onChange={(e) => {
              setCurrency(e.target.value);
              setWalletCurr(currency);
            }}
            sx={{ width: "250", color: "black", flex: 1 }}
          >
            <MenuItem disabled value="">
              <em>Currency</em>
            </MenuItem>
            {currencies.map((curr) => (
              <MenuItem value={curr}>{curr}</MenuItem>
            ))}
          </Select>
        </Box>
        <WalletCard
          walletName={name ? name : "Wallet"}
          description="This is your first wallet! You will be able to access it once you finish setting up your account."
          buttons={[]}
          balance="0.00"
          currency={currency}
        ></WalletCard>
      </Paper>
    </>
  );
}
