import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { apiUrl, baseUrl } from "../../shared.js";
import SendIcon from "@mui/icons-material/Send";
import { Avatar, Tooltip, Typography } from "@mui/material";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import PersonRemoveIcon from "@mui/icons-material/PersonRemove";
import CallReceivedIcon from "@mui/icons-material/CallReceived";
import Transaction from "./Transaction.tsx";
import { useState } from "react";
import Button from "@mui/material/Button/Button";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  borderRadius: "6px",
  boxShadow: 24,
  p: 4,
  display: "flex",
  flexDirection: "column",
  gap: "10px",
};

type dataState = [boolean, (e: boolean) => boolean];

interface Props {
  open: dataState;
  friend: Friend;
}

export default function FriendView(props: Props) {
  const [open, setOpen] = props.open;

  const [transactionOpen, setTransactionOpen] = useState(false);
  const handleTransactionOpen = (value: boolean) => {
    setTransactionOpen(value);
    return value;
  };

  const friend = props.friend;

  const handleClose = () => {
    setOpen(false);
    setTransactionOpen(false);
  };

  return (
    <Modal
      aria-labelledby="transition-modal-title"
      aria-describedby="transition-modal-description"
      open={open}
      onClose={handleClose}
      closeAfterTransition
      slots={{ backdrop: Backdrop }}
      slotProps={{
        backdrop: {
          timeout: 500,
        },
      }}
    >
      <Box sx={style}>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "30px",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: "20px" }}>
            <Avatar
              alt={friend?.username}
              src={`${baseUrl}static/avatars/${friend.id}.png`}
            />
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-end",
              }}
            >
              <Typography variant="h6">
                {friend.f_name} {friend.l_name}
              </Typography>
            </Box>
          </Box>
          <Tooltip title="Unfriend">
            <PersonRemoveIcon
              fontSize="medium"
              sx={{ color: "black", cursor: "pointer" }}
              onClick={() => {}}
            />
          </Tooltip>
        </Box>
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <ButtonBlack
            invert
            sx={{ width: "150px", paddingX: "5px" }}
            variant="outlined"
            onClick={() => {
              setTransactionOpen(!transactionOpen);
            }}
          >
            Send money
          </ButtonBlack>
          <ButtonBlack
            invert
            sx={{ width: "150px", paddingX: "5px" }}
            variant="outlined"
          >
            Request money
          </ButtonBlack>
        </Box>
        {transactionOpen && (
          <Transaction
            friend={friend}
            transactionOpen={[transactionOpen, handleTransactionOpen]}
          ></Transaction>
        )}
      </Box>
    </Modal>
  );
}
