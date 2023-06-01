import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import WalletIcon from "@mui/icons-material/Wallet";
import { Wallet } from "../../pages/Profile";

export default function SelectSmall({
  wallets,
  setWallet,
  invert,
}: {
  wallets: Wallet[];
  setWallet: (wallet: Wallet | undefined) => void;
  invert?: boolean;
}) {
  const [selectedWalletId, setSelectedWalletId] = React.useState<string>();

  const handleChange = (event: SelectChangeEvent<string>) => {
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
        <MenuItem>
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
