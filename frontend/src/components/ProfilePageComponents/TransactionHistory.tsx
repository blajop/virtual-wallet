import Paper from "@mui/material/Paper/Paper";
import axios from "axios";
import { useEffect, useState } from "react";
import { apiUrl } from "../../shared";
import Box from "@mui/material/Box/Box";
import Typography from "@mui/material/Typography/Typography";
import retrieveUser from "../../functions/retrieveUser.ts";
import { Friend } from "../components/ProfilePageComponents/FriendBox";

type User = Friend;

export interface Transaction {
  wallet_sender: string;
  card_sender: string;
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

function TransactionHistory() {
  const [transactions, setTransactions] = useState<Transaction[]>();
  const [sendingUsers, setSendingUsers] = useState<User[]>([]);
  const [receivingUsers, setReceivingUsers] = useState<User[]>([]);

  useEffect(() => {
    axios
      .get(apiUrl + "transactions", {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      })
      .then((response) => {
        setTransactions(response.data);
      });
  }, []);

  useEffect(() => {
    const fetchSenders = async () => {
      if (transactions) {
        const fetchedUsers = await Promise.all(
          transactions.map((transaction) =>
            retrieveUser(transaction.sending_user)
          )
        );
        setSendingUsers(fetchedUsers);
      }
    };
    const fetchReceivers = async () => {
      if (transactions) {
        const fetchedUsers = await Promise.all(
          transactions.map((transaction) =>
            retrieveUser(transaction.receiving_user)
          )
        );
        setSendingUsers(fetchedUsers);
      }
    };

    fetchSenders();
    fetchReceivers();
  }, [transactions]);

  return (
    <Paper elevation={2} sx={{ height: "100%", padding: "20px" }}>
      {transactions?.map((transaction, index) => (
        <Box key={transaction.id}>
          <Typography>{transaction.id}</Typography>
          <Typography>{users[index]?.f_name}</Typography>
        </Box>
      ))}
    </Paper>
  );
}

export default TransactionHistory;
