import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container/Container";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { useEffect, useState } from "react";
import { baseUrl } from "../shared.js";
import Divider from "@mui/material/Divider";
import WalletCard from "../components/Wallet/WalletCard.js";
import SelectSmall from "../components/Select/Select";

export default function Profile() {
  //   let fullName = "";
  //   let email = "";
  //   let phone = "";
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [wallets, setWallets] = useState([]);
  const [wallet, setWallet] = useState();

  const handleSelectWallet = (selectedWallet) => {
    setWallet(selectedWallet); // Set the entire selected wallet object
  };

  useEffect(() => {
    //   GET USER
    axios
      .get(baseUrl + "api/v1/users/profile", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((response) => {
        if (response.status === 200) {
          setFullName(`${response.data.f_name} ${response.data.l_name}`);
          setEmail(response.data.email);
          setPhone(response.data.phone);

          //   GET WALLETS

          axios
            .get(baseUrl + `api/v1/users/${response.data.email}/wallets`, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            })
            .then((response) => {
              if (response.status === 200) {
                setWallets(response.data);
              }
            })
            .catch();
        }
      })
      .catch();
  }, []);

  //   Update wallet
  useEffect(() => {
    console.log("Selected Wallet:", wallet);
  }, [wallet]);

  return (
    <Container
      maxWidth="md"
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        border: "solid, black, 1px",
        height: "50vh",
        backgroundColor: "gray",
        position: "absolute",
        gap: "20px",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        paddingY: "50px",
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: "50px" }}>
        <Avatar
          src={localStorage.getItem("avatar")}
          sx={{ height: "80px", width: "80px" }}
        ></Avatar>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: "bold" }}>
            {fullName}
          </Typography>
          <Typography
            variant="body1"
            sx={{ marginBottom: "-5px", fontStyle: "italic" }}
          >
            {email}
          </Typography>
          <Typography variant="body1" sx={{ fontStyle: "italic" }}>
            {phone}
          </Typography>
        </Box>
      </Box>
      <hr className="w-[80%] text-black border-2" />
      <Box
        sx={{
          backgroundColor: "white",
          height: "200px",
          width: "500px",
        }}
      >
        <SelectSmall wallets={wallets} setWallet={handleSelectWallet} />
      </Box>
      {wallet && (
        <WalletCard
          name={fullName}
          currency={wallet.currency.toUpperCase()}
          balance={wallet.balance.toFixed(2)}
          walletName={wallet.name}
        ></WalletCard>
      )}
    </Container>
  );
}
