import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import WalletIcon from "@mui/icons-material/Wallet";

export default function SelectSmall({ wallets, setWallet, invert }) {
  const [selectedWalletId, setSelectedWalletId] = React.useState();

  const handleChange = (event) => {
    setSelectedWalletId(event.target.value);
    const selectedWallet = wallets.find(
      (wallet) => wallet.id === event.target.value
    );
    setWallet(selectedWallet); // Pass the selected wallet object to the callback function
  };

  return (
    <FormControl
      sx={{
        mt: 1,
        width: "100%",
        backgroundColor: invert ? "black" : "white",
        color: invert ? "white" : "black",
        display: "flex",
        paddingY: "0px",
      }}
      size="small"
    >
      <Select
        displayEmpty={true}
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={selectedWalletId}
        onChange={handleChange}
        sx={{
          color: invert ? "white" : "black",
        }}
      >
        <MenuItem value={wallets[0]}>
          <em>None</em>
        </MenuItem>
        {wallets.map((wallet, index) => (
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
