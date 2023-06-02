import Box from "@mui/material/Box";
import Container from "@mui/material/Container/Container";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { useEffect, useState } from "react";
import { baseUrl } from "../shared.js";
import WalletCard from "../components/Wallet/WalletCard.js";
import SelectSmall from "../components/Select/Select";
import { Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CircularLoading from "../components/CircularLoading.js";
import FriendBox from "../components/FriendBox.js";
import CustomAvatar from "../components/Icons/CustomAvatar.tsx";

export type Wallet = {
  id: string;
  name?: string;
  currency: string;
  balance: number;
};

export type DefWallet = {
  id: string;
  name?: string;
  currency: string;
  balance: number;
};

type WalletResponse = Wallet[];

type UserResponse = {
  f_name: string;
  l_name: string;
  email: string;
  phone: string;
};

export default function Profile() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);

  const [fullName, setFullName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [, setPhone] = useState<string>("");
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [wallet, setWallet] = useState<Wallet | undefined>();

  const handleSelectWallet = (wallet: Wallet | undefined) => {
    setWallet(wallet);
  };

  useEffect(() => {
    setLoading(true);

    //   GET USER
    const getUser = async () => {
      try {
        const response = await axios.get<UserResponse>(
          baseUrl + "api/v1/users/profile",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );

        if (response.status === 200) {
          setFullName(`${response.data.f_name} ${response.data.l_name}`);
          setEmail(response.data.email);
          setPhone(response.data.phone);

          setLoading(true);
          await getWallets(response.data.email);
          await getDefaultWallet(response.data.email);
        }
      } catch (error) {
        navigate("/");
      } finally {
        setTimeout(() => {
          setLoading(false);
        }, 300);
      }
    };

    getUser();
  }, []);
  //   GET WALLETS
  const getWallets = async (email: string) => {
    try {
      const response = await axios.get<WalletResponse>(
        baseUrl + `api/v1/users/${email}/wallets`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.status === 200) {
        setWallets(response.data);
      }
    } catch (error) {
      // Handle error
    }
  };
  //   GET DEFAULT WALLET
  const getDefaultWallet = async (email: string) => {
    try {
      const response = await axios.get<DefWallet>(
        baseUrl + `api/v1/users/${email}/wallets/default`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (response.status === 200) {
        setWallet(response.data);
      }
    } catch (error) {
      // Handle error
    }
  };

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
        <CustomAvatar />
        <Typography variant="h3" sx={{ fontWeight: "700" }}>
          {fullName}
        </Typography>
      </Paper>
      {/* WALLETS  */}
      <Container
        sx={{
          display: "flex",
          alignItems: "flex-start",
          gap: "20px",
          padding: "0 !important",
        }}
      >
        <>
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
              {loading ? (
                <CircularLoading />
              ) : (
                <>
                  <WalletCard
                    username={email}
                    walletId={wallet?.id ?? ""}
                    currency={wallet?.currency.toUpperCase()}
                    balance={wallet?.balance.toFixed(2)}
                    walletName={wallet?.name || "Wallet"}
                  />

                  <SelectSmall
                    wallets={wallets}
                    setWallet={handleSelectWallet}
                  />
                </>
              )}
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
            <FriendBox email={email} />
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
        </>
      </Container>
    </Container>
  );
}
