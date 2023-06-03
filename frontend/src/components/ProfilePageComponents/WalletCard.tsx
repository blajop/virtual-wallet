import Avatar from "@mui/material/Avatar/Avatar";
import AvatarGroup from "@mui/material/AvatarGroup/AvatarGroup";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import ButtonBlack from "../Buttons/ButtonBlack.js";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import SendIcon from "@mui/icons-material/Send";
import AddIcon from "@mui/icons-material/Add";
import Tooltip from "@mui/material/Tooltip/Tooltip";
import axios from "axios";
import { useEffect, useState } from "react";
import { baseUrl } from "../../shared.js";

interface CardProps {
  name?: string;
  walletName?: string;
  description?: string;
  currency?: string;
  balance?: string;
  walletId?: string;
  username?: string;
  invert?: boolean;
  buttons?: string[];
}

type Leech = {
  id: number;
  username: string;
};

export default function WalletCard(props: CardProps) {
  const name = props.name;
  const walletName = props.walletName;
  const description = props.description;
  const currency = props.currency;
  const balance = props.balance;
  const walletId = props.walletId;
  const username = props.username;
  const invert = props.invert || false;
  const buttons = props.buttons || [`deposit`, `send`, `invite`];

  const [leeches, setLeeches] = useState<Leech[]>([]);

  const requestUrl =
    baseUrl + `api/v1/users/${username}/wallets/${walletId}/leeches`;

  useEffect(() => {
    if (username) {
      axios
        .get(requestUrl, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((response) => {
          setLeeches(response.data);
        });
    }
  }, [walletId]);

  return (
    <Card
      sx={{
        minWidth: 500,
        padding: "1rem",
        backgroundColor: invert ? "black" : "white",
      }}
    >
      <CardContent>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderBottom: invert ? "solid white 1px" : "solid black 1px",
          }}
        >
          <Typography
            variant="h5"
            component="div"
            sx={{ color: invert ? "white" : "black" }}
          >
            {walletName}
          </Typography>
          <Typography variant="h5" sx={{ color: invert ? "white" : "black" }}>
            {balance} {currency}
            <br />
          </Typography>
        </Box>
        {name && (
          <Typography
            variant="h5"
            component="div"
            sx={{ color: invert ? "white" : "black" }}
          >
            {name}
          </Typography>
        )}
        <Box
          sx={{ display: "flex", justifyContent: "space-between", mt: "20px" }}
        >
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              gap: "5px",
            }}
          >
            {description && <Typography variant="h6">{description}</Typography>}
            {buttons && buttons.includes("deposit") && (
              <Tooltip title={"Add money"}>
                <span>
                  <ButtonBlack invert={invert}>
                    <AddIcon
                      fontSize="medium"
                      sx={{ color: invert ? "black" : "white" }}
                    />
                  </ButtonBlack>
                </span>
              </Tooltip>
            )}

            {buttons && buttons.includes("send") && (
              <Tooltip title={"Send money"}>
                <span>
                  <ButtonBlack invert={invert}>
                    <SendIcon
                      fontSize="medium"
                      sx={{ color: invert ? "black" : "white" }}
                    />
                  </ButtonBlack>
                </span>
              </Tooltip>
            )}
            {buttons && buttons.includes("invite") && (
              <Tooltip title={"Invite people"}>
                <span>
                  <ButtonBlack invert={invert}>
                    <PersonAddIcon
                      fontSize="medium"
                      sx={{ color: invert ? "black" : "white" }}
                    />
                  </ButtonBlack>
                </span>
              </Tooltip>
            )}
          </Box>

          <AvatarGroup max={4}>
            {leeches.map((leech, index) => (
              <Avatar
                key={index}
                alt={leech.username}
                src={`${baseUrl}static/avatars/${leech.id}.png`}
              />
            ))}
          </AvatarGroup>
        </Box>
      </CardContent>
    </Card>
  );
}