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
import { AvatarGroup, Paper } from "@mui/material";

export default function Profile() {
  //   let fullName = "";
  //   let email = "";
  //   let phone = "";
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [wallets, setWallets] = useState([]);
  const [wallet, setWallet] = useState();
  const [defaultWallet, setDefaultWallet] = useState();

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
          console.log(response.data);
          //   setDefaultWallet(response.data.user_settings);

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
                console.log(response.data);
              }
            })
            .catch();
        }
      })
      .catch();
  }, []);

  //   Update wallet
  useEffect(() => {}, [wallet]);

  return (
    <Container
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        height: "auto",
        width: "auto",
        backgroundColor: "white",
        gap: "40px",
        paddingY: "50px",
      }}
    >
      <Paper
        elevation={2}
        sx={{
          display: "flex",
          alignItems: "center",
          gap: "50px",
          height: "100%",
          width: "100%",
          padding: "20px",
        }}
      >
        <Avatar
          src={localStorage.getItem("avatar")}
          sx={{ height: "80px", width: "80px" }}
        ></Avatar>
        <Typography variant="h3" sx={{ fontWeight: "700" }}>
          {fullName}
        </Typography>
      </Paper>
      {/* WALLETS */}
      <Container
        sx={{
          display: "flex",
          alignItems: "flex-start",
          gap: "20px",
          padding: "0 !important",
        }}
      >
        <Box>
          <Paper
            elevation={2}
            sx={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              backgroundColor: "white",
              height: "auto",
              width: "auto",
              padding: "20px",
            }}
          >
            {wallet && (
              <WalletCard
                username={email}
                walletId={wallet.id}
                currency={wallet.currency.toUpperCase()}
                balance={wallet.balance.toFixed(2)}
                walletName={wallet.name || "Wallet"}
              />
            )}
            <SelectSmall wallets={wallets} setWallet={handleSelectWallet} />
            {/* CARDS */}
            <br />
            {wallet && (
              <WalletCard
                username={email}
                walletId={wallet.id}
                currency={wallet.currency.toUpperCase()}
                balance={wallet.balance.toFixed(2)}
                walletName={wallet.name || "Wallet"}
              />
            )}
            <SelectSmall wallets={wallets} setWallet={handleSelectWallet} />
          </Paper>
        </Box>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            flex: "1 !important",
            height: "100% !important",
          }}
        >
          <Paper
            elevation={2}
            sx={{
              display: "flex",
              justifyContent: "center",
              backgroundColor: "white",
              height: "100% !important",
              width: "auto",
              padding: "20px",
              flex: "0 !important",
            }}
          >
            <AvatarGroup max={6}>
              <Avatar alt="Remy Sharp" src="/static/images/avatar/1.jpg" />
              <Avatar alt="Travis Howard" src="/static/images/avatar/2.jpg" />
              <Avatar alt="Cindy Baker" src="/static/images/avatar/3.jpg" />
              <Avatar alt="Agnes Walker" src="/static/images/avatar/4.jpg" />
              <Avatar alt="Cindy Baker" src="/static/images/avatar/3.jpg" />
              <Avatar alt="Agnes Walker" src="/static/images/avatar/4.jpg" />
              <Avatar
                alt="Trevor Henderson"
                src="/static/images/avatar/5.jpg"
              />
            </AvatarGroup>
          </Paper>
          <br></br>
          <Paper
            elevation={2}
            sx={{
              display: "flex !important",
              flexDirection: "column",
              justifyContent: "center",
              backgroundColor: "white",
              height: "100% !important",
              width: "auto",
              padding: "20px",
              flex: "1 !important",
            }}
          >
            {wallet && (
              <WalletCard
                username={email}
                walletId={wallet.id}
                currency={wallet.currency.toUpperCase()}
                balance={wallet.balance.toFixed(2)}
                walletName={wallet.name || "Wallet"}
              />
            )}
            <SelectSmall wallets={wallets} setWallet={handleSelectWallet} />
          </Paper>
        </Box>
      </Container>
    </Container>
  );
}
