import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Transaction from "./Transaction.tsx";
import Typography from "@mui/material/Typography/Typography";
import { useEffect, useState } from "react";
import retrieveUser from "../../functions/retrieveUser.ts";
import { Friend } from "../ProfilePageComponents/FriendBox.tsx";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";
import { formatDateTime } from "../ProfilePageComponents/TransactionRecurring.tsx";

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
}

type dataState = [boolean, (e: boolean) => void];

interface Props {
  open: dataState;
  transaction: Transaction;
  username: string;
}

export default function TransactionDetail(props: Props) {
  const [open, setOpen] = props.open;
  const transaction = props.transaction;

  const [, setSender] = useState<Friend>();
  const [receiver, setReceiver] = useState<Friend>();

  const handleClose = () => {
    setOpen(false);
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
      <Box sx={style}>
        {transaction.recurring === "Monthly"
          ? receiver && (
              <Typography>
                Recurring transaction for {transaction.amount.toFixed(2)}{" "}
                {transaction.currency} to {receiver.f_name} {receiver.l_name}.
                Next billing is on {formatDateTime(transaction.created).day}{" "}
                {formatDateTime(transaction.created, true).month}
              </Typography>
            )
          : receiver && (
              <Typography>
                Recurring transaction for {transaction.amount.toFixed(2)}{" "}
                {transaction.currency} to {receiver.f_name} {receiver.l_name}.
                Next billing is on {formatDateTime(transaction.created).day}{" "}
                {formatDateTime(transaction.created).month}{" "}
                {new Date().getFullYear() + 1}
              </Typography>
            )}
        <Box sx={{ display: "flex", gap: "10px" }}>
          <ButtonBlack>Cancel payment</ButtonBlack>
        </Box>
      </Box>
    </Modal>
  );
}
