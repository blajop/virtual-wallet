import Box from "@mui/material/Box";
import Container from "@mui/material/Container/Container";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { useEffect, useState } from "react";
import { baseUrl } from "../shared.js";
import WalletCard from "../components/ProfilePageComponents/WalletCard.js";
import SelectSmall from "../components/Select/Select";
import { Card, CardContent, Grid, Paper, Tooltip } from "@mui/material";
import { useNavigate } from "react-router-dom";
import CircularLoading from "../components/CircularLoading.js";
import FriendBox from "../components/ProfilePageComponents/FriendBox.js";
import CustomAvatar from "../components/Icons/CustomAvatar.tsx";
import EditProfile from "../components/ProfilePageComponents/EditProfile.tsx";
import Cards from "../components/ProfilePageComponents/Cards.tsx";
import SelectCard from "../components/Select/SelectCard.tsx";
import TransactionPanel from "../components/ProfilePageComponents/TransactionPanel.tsx";
import ButtonBlack from "../components/Buttons/ButtonBlack.tsx";
import AddIcon from "@mui/icons-material/Add";

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

export type Card = {
  number: string;
  expiry: string;
  holder: string;
  cvc: string;
  id: string;
};

type UserResponse = {
  f_name: string;
  l_name: string;
  email: string;
  phone: string;
  username: string;
};

export default function Profile() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const [refreshFriends, setRefreshFriends] = useState<boolean>(false);

  const handleRefreshFriends = () => {
    setRefreshFriends(!refreshFriends);
  };

  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [phone, setPhone] = useState<string>("");

  const [wallet, setWallet] = useState<Wallet | undefined>();
  const [card, setCard] = useState<Card | undefined>();

  const handleSelectWallet = (wallet: Wallet | undefined) => {
    setWallet(wallet);
  };

  const handleSelectCard = (card: Card | undefined) => {
    setCard(card);
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
          setFirstName(response.data.f_name);
          setLastName(response.data.l_name);
          setUsername(response.data.username);
          setEmail(response.data.email);
          setPhone(response.data.phone);

          setLoading(true);
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
          justifyContent: "space-between",
          gap: "50px",
          height: "100%",
          width: "100%",
          padding: "20px",
        }}
      >
        <Box className="flex items-center gap-5">
          <CustomAvatar />
          <Typography variant="h3" sx={{ fontWeight: "700" }}>
            {`${firstName} ${lastName}`}
          </Typography>
        </Box>

        <EditProfile
          firstName={[
            firstName,
            (value: string) => {
              setFirstName(value);
              return value;
            },
          ]}
          lastName={[
            lastName,
            (value: string) => {
              setLastName(value);
              return value;
            },
          ]}
          username={username}
          email={[
            email,
            (value: string) => {
              setEmail(value);
              return value;
            },
          ]}
          phone={[
            phone,
            (value: string) => {
              setPhone(value);
              return value;
            },
          ]}
        />
      </Paper>
      {/* WALLETS  */}
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
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

                <Box sx={{ display: "flex", gap: "10px" }}>
                  <Tooltip title={"Create a new wallet"}>
                    <span className="mt-[8px]">
                      <ButtonBlack
                        invert
                        sx={{ height: "100%", borderColor: "lightgray" }}
                      >
                        <AddIcon />
                      </ButtonBlack>
                    </span>
                  </Tooltip>
                  <SelectSmall
                    username={username}
                    setWallet={handleSelectWallet}
                    refreshFriends={refreshFriends}
                  />
                </Box>
              </>
            )}
            {/* CARDS */}
            <br />
            {card ? (
              <Cards
                holder={card.holder}
                number={card.number}
                exp={new Date(card.expiry)}
              />
            ) : (
              <Card
                sx={{
                  padding: "1rem",
                  backgroundColor: "white",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <CardContent>
                  <Paper
                    sx={{
                      width: "344px",
                      height: " 186px",
                      borderRadius: "10px",
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                      backgroundColor: "white",
                    }}
                  >
                    <Typography variant="h5">No cards added yet</Typography>
                    <Typography variant="body2">
                      start by clicking the + button bellow!
                    </Typography>
                  </Paper>
                </CardContent>
              </Card>
            )}
            <Box sx={{ display: "flex", gap: "10px" }}>
              <Tooltip title={"Add a new card"}>
                <span className="mt-[8px]">
                  <ButtonBlack
                    invert
                    sx={{ height: "100%", borderColor: "lightgray" }}
                  >
                    <AddIcon />
                  </ButtonBlack>
                </span>
              </Tooltip>
              <SelectCard
                username={username}
                token={localStorage.token}
                setCard={handleSelectCard}
              />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper
            elevation={2}
            sx={{
              display: "flex",
              flexDirection: "column",
              height: "100% !important",
              width: "auto",
              padding: "20px",
            }}
          >
            <FriendBox
              refreshFriends={refreshFriends}
              handleRefreshFriends={handleRefreshFriends}
              email={email}
            />
            <br></br>
            <TransactionPanel
              username={username}
              refreshFr={[refreshFriends, setRefreshFriends]}
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
