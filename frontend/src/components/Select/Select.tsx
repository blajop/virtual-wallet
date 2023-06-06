import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import WalletIcon from "@mui/icons-material/Wallet";
import { Wallet } from "../../pages/Profile";
import axios from "axios";
import { apiUrl } from "../../shared";

export default function SelectSmall({
  username,
  setWallet,
}: {
  username: string;
  setWallet: (wallet: Wallet | undefined) => void;
}) {
  const [selectedWalletId, setSelectedWalletId] = React.useState<string>("");
  const [allWallets, setAllWallets] = React.useState<Wallet[]>([]);

  React.useEffect(() => {
    if (username)
      axios
        .get<Wallet[]>(apiUrl + `users/${username}/wallets`, {
          headers: {
            Authorization: `Bearer ${localStorage.token}`,
          },
        })
        .then((response) => {
          setAllWallets(response.data);
          if (response.data.length > 0) {
            setWallet(response.data[0]);
            setSelectedWalletId(response.data[0].id);
          }
        });
  }, [username]);

  const handleChange = (event: SelectChangeEvent<string>) => {
    setSelectedWalletId(event.target.value);
    const selectedWallet = allWallets.find(
      (wallet) => wallet.id === event.target.value
    );
    setWallet(selectedWallet);
  };

  return (
    <FormControl
      sx={{
        mt: 1,
        width: "100%",
        backgroundColor: "white",
        color: "black",
        display: "flex",
        paddingY: "0px",
      }}
      size="small"
    >
      <Select
        displayEmpty={false}
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={selectedWalletId}
        onChange={handleChange}
        sx={{
          color: "black",
        }}
      >
        {allWallets.map((wallet, index) => (
          <MenuItem
            key={index}
            value={wallet.id}
            sx={{
              display: "flex",
              alignItems: "center",
            }}
          >
            <WalletIcon /> {"  "}
            {wallet.name || "Wallet"} | {wallet.balance.toFixed(2)}{" "}
            {wallet.currency.toUpperCase()}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
