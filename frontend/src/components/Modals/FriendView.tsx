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

  const friend = props.friend;

  const handleClose = () => {
    setOpen(false);
    setTransactionOpen(false);
  };

  //   const handleSend = () => {

  //     const finalData = {

  //     };
  //     axios
  //       .put(`${baseUrl}api/v1/users/profile`, finalData, {
  //         headers: {
  //           Authorization: `Bearer ${localStorage.getItem("token")}`,
  //         },
  //       })
  //       .then((response) => {
  //         if (response.status === 200) {
  //           console.log(response);
  //         }
  //       })
  //       .catch();
  //     handleClose();
  //   };

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
        <Avatar
          sx={{ cursor: "pointer" }}
          alt={friend?.username}
          src={`${baseUrl}static/avatars/${friend.id}.png`}
        />
        <Typography>
          {friend.f_name} {friend.l_name}
        </Typography>
        <Box sx={{ display: "flex", gap: "20px" }}>
          <Tooltip title="Send money">
            <SendIcon
              fontSize="medium"
              sx={{ color: "black", cursor: "pointer" }}
              onClick={() => {
                setTransactionOpen(!transactionOpen);
              }}
            />
          </Tooltip>

          <Tooltip title="Request money">
            <CallReceivedIcon
              fontSize="medium"
              sx={{
                color: "black",
                cursor: "pointer",
              }}
              onClick={() => {}}
            />
          </Tooltip>
          <Tooltip title="Unfriend">
            <PersonRemoveIcon
              fontSize="medium"
              sx={{ color: "black", cursor: "pointer" }}
              onClick={() => {}}
            />
          </Tooltip>
        </Box>
        {transactionOpen && <Transaction friend={friend}></Transaction>}
      </Box>
    </Modal>
  );
}
