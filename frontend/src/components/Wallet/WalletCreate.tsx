import TextField from "@mui/material/TextField";
import { Fragment, useState } from "react";
import axios from "axios";
import Typography from "@mui/material/Typography";
import WalletCard from "./WalletCard";

interface WallProps {
  f_name: string;
  l_name: string;
}

export default function WalletCreate(props: WallProps) {
  const f_name = props.f_name;
  const l_name = props.l_name;
  const [formWall, setFormWall] = useState({
    wallet_name: "",
    currency: "",
  });

  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormWall({ ...formWall, [event.target.name]: event.target.value });
  };

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    axios
      .post("http://localhost:8000/api/v1/signup", formWall)
      .then((response) => {
        if (response.status === 200) {
          setTimeout(() => {
            // navigate("/home");
          }, 3000);
        }
      });
  }

  return {
    formWall,
    renderWall: (
      <Fragment>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Typography
            variant="h5"
            sx={{
              marginTop: "80px",
              letterSpacing: 0.6,
            }}
            className="text-black font-bold"
          >
            Create your first wallet
          </Typography>
        </div>
        <form
          id="form"
          className="flex justify-center mt-20"
          onSubmit={handleSubmit}
        >
          <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] flex flex-col">
            <TextField
              required
              name="wallet_name"
              label="Wallet name"
              onChange={handleInput}
            />
          </div>

          <div className="w-[350px] justify-center gap-[10px] rounded p-[40px] flex flex-col">
            <TextField
              required
              label="Currency"
              name="currency"
              autoComplete="transaction-currency"
              onChange={handleInput}
            />
          </div>
        </form>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <WalletCard
            name={`${f_name} ${l_name}`}
            walletName={formWall["wallet_name"]}
            currency={formWall["currency"]}
            walletId={""}
            username={""}
          />
        </div>
      </Fragment>
    ),
  };
}
