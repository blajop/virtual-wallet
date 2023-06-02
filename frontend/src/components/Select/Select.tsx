import * as React from "react";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import WalletIcon from "@mui/icons-material/Wallet";
import { Wallet, DefWallet } from "../../pages/Profile";

export default function SelectSmall({
  wallets,
  defaultWallet,
  setWallet,
  invert,
}: {
  wallets: Wallet[];
  defaultWallet: DefWallet | undefined;
  setWallet: (wallet: Wallet | undefined) => void;
  invert?: boolean;
}) {
  const [selectedWalletId, setSelectedWalletId] = React.useState<string>(""); // Initialize with an empty string

  const handleChange = (event: SelectChangeEvent<string>) => {
    setSelectedWalletId(event.target.value);
    const selectedWallet = wallets.find(
      (wallet) => wallet.id === event.target.value
    );
    setWallet(selectedWallet);
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
        displayEmpty={false}
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={selectedWalletId}
        defaultValue={defaultWallet?.id}
        onChange={handleChange}
        sx={{
          color: invert ? "white" : "black",
        }}
      >
        <MenuItem
          key={0}
          value={defaultWallet?.id}
          sx={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <WalletIcon /> {"  "}
          {defaultWallet?.name || "Wallet"} |{" "}
          {defaultWallet?.balance.toFixed(2)}{" "}
          {defaultWallet?.currency.toUpperCase()}
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
