import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

export default function SelectSmall({ wallets, setWallet }) {
  const [selectedWalletId, setSelectedWalletId] = React.useState("");

  const handleChange = (event) => {
    setSelectedWalletId(event.target.value);
    const selectedWallet = wallets.find(
      (wallet) => wallet.id === event.target.value
    );
    setWallet(selectedWallet); // Pass the selected wallet object to the callback function
  };

  return (
    <FormControl sx={{ m: 1, width: 200 }} size="small">
      <Select
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={selectedWalletId}
        label="Age"
        onChange={handleChange}
      >
        <MenuItem value="">
          <em>None</em>
        </MenuItem>
        {wallets.map((wallet, index) => (
          <MenuItem key={index} value={wallet.id}>
            {wallet.name || "Wallet"} • {wallet.balance.toFixed(2)} •{" "}
            {wallet.currency.toUpperCase()}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
