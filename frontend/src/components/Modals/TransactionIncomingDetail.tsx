import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Transaction from "./Transaction.tsx";
import Typography from "@mui/material/Typography/Typography";
import { useEffect, useState } from "react";
import retrieveUser from "../../functions/retrieveUser.ts";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";
import axios from "axios";
import { apiUrl } from "../../shared.ts";

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

export interface Transaction {
  wallet_sender: string;
  card_sender: string;
  receiving_user: string;
  wallet_receiver: string;
  currency: string;
  amount: number;
  recurring: string;
  detail: string;
  sending_user: string;
  id: string;
  status: string;
  spending_category_id: number;
  created: string;
  updated: string;
  link_accept: string;
  link_decline: string;
}

type dataState = [boolean, (e: boolean) => void];

interface Props {
  open: dataState;
  transaction: Transaction;
  username: string;
  refresh: dataState;
}

export default function TransactionDetail(props: Props) {
  const [open, setOpen] = props.open;
  const transaction = props.transaction;
  const username = props.username;
  const [refresh, setRefresh] = props.refresh;

  const [cancelled, setCancelled] = useState(false);
  const [declined, setDeclined] = useState(false);
  const [accepted, setAccepted] = useState(false);

  const [sender, setSender] = useState<Friend>();
  const [receiver, setReceiver] = useState<Friend>();

  const handleClose = () => {
    setOpen(false);
  };

  const handleCancel = () => {
    try {
      axios
        .put(apiUrl + `transactions/${transaction.id}/cancel`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.token}`,
          },
        })
        .then((response) => {
          if (response.status === 200) {
            setCancelled(true);
            setRefresh(!refresh);
            setTimeout(() => {
              setCancelled(false);
              handleClose();
            }, 3000);
          }
        });
    } catch (error) {
      console.log(error);
    }
  };

  const handleDecline = () => {
    try {
      axios
        .get(apiUrl + transaction.link_decline, {
          headers: {
            Authorization: `Bearer ${localStorage.token}`,
          },
        })
        .then((response) => {
          if (response.status === 200) {
            setDeclined(true);
            setRefresh(!refresh);
            setTimeout(() => {
              setDeclined(false);
              handleClose();
            }, 3000);
          }
        });
    } catch (error) {
      console.log(error);
    }
  };

  const handleAccept = () => {
    try {
      axios
        .get(apiUrl + transaction.link_accept, {
          headers: {
            Authorization: `Bearer ${localStorage.token}`,
          },
        })
        .then((response) => {
          if (response.status === 200) {
            setAccepted(true);
            setRefresh(!refresh);
            setTimeout(() => {
              setAccepted(false);
              handleClose();
            }, 3000);
          }
        });
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const fetchSender = async () => {
      if (transaction) {
        const fetchedSender = await retrieveUser(transaction.sending_user);
        const fetchedReceiver = await retrieveUser(transaction.receiving_user);
        setSender(fetchedSender);
        setReceiver(fetchedReceiver);
      }
    };
    fetchSender();
  }, [transaction]);

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
      {sender && receiver && sender.username !== username ? (
        <Box sx={style}>
          {sender && (
            <Typography>
              {sender.f_name} {sender.l_name} is trying to send you{" "}
              {transaction.amount.toFixed(2)} {transaction.currency}
            </Typography>
          )}
          <Box sx={{ display: "flex", gap: "10px" }}>
            <ButtonBlack onClick={handleAccept}>Accept</ButtonBlack>
            <ButtonBlack onClick={handleDecline}>Decline</ButtonBlack>
          </Box>
          <Typography>{declined && "Transaction declined!"}</Typography>
          <Typography>{accepted && "Transaction accepted!"}</Typography>
        </Box>
      ) : (
        <Box sx={style}>
          {receiver && (
            <Typography>
              You have sent {transaction.amount.toFixed(2)}{" "}
              {transaction.currency} to {receiver.f_name} {receiver.l_name}.
            </Typography>
          )}
          <Box sx={{ display: "flex", gap: "10px" }}>
            <ButtonBlack onClick={handleCancel}>I changed my mind</ButtonBlack>
          </Box>
          <Typography>{cancelled && "Transaction cancelled!"}</Typography>
        </Box>
      )}
    </Modal>
  );
}
