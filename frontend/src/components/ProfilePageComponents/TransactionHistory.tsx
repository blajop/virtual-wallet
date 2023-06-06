import Paper from "@mui/material/Paper/Paper";
import axios from "axios";
import { useEffect, useState } from "react";
import { apiUrl } from "../../shared";
import Box from "@mui/material/Box/Box";
import Typography from "@mui/material/Typography/Typography";
import retrieveUser from "../../functions/retrieveUser.ts";
import { Friend } from "./FriendBox";
import LocalAtmIcon from "@mui/icons-material/LocalAtm";
import CreditCardIcon from "@mui/icons-material/CreditCard";
import LocalDiningIcon from "@mui/icons-material/LocalDining";
import React from "react";
import Pagination from "@mui/material/Pagination/Pagination";

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
  receiving_user: string;
  id: string;
  status: string;
  spending_category_id: number;
  created: string;
  updated: string;
}

type CustomDate = { day: string; month: string };

function formatDateTime(dateTime: string): CustomDate {
  const date = new Date(dateTime);
  const day = date.getDate().toString();
  const monthAbbreviations = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  const month = monthAbbreviations[date.getMonth()];

  return { day: day, month: month };
}

const spendingIcons = [
  <CreditCardIcon />,
  <LocalDiningIcon />,
  <LocalAtmIcon />,
];

function TransactionHistory({ username }: { username: string }) {
  const [transactions, setTransactions] = useState<Transaction[]>();
  const [sendingUsers, setSendingUsers] = useState<User[]>([]);
  const [receivingUsers, setReceivingUsers] = useState<User[]>([]);

  const [page, setPage] = useState<number>(1);
  const [pageNumber, setPageNumber] = useState<number>();

  useEffect(() => {
    axios
      .get(apiUrl + `transactions?size=5&page=${page}`, {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      })
      .then((response) => {
        setPageNumber(response.data.pages);
        setTransactions(response.data.items);
      });
  }, [page]);

  useEffect(() => {
    const fetchSenders = async () => {
      if (transactions) {
        const fetchedSenders = await Promise.all(
          transactions.map((transaction) =>
            retrieveUser(transaction.sending_user)
          )
        );
        setSendingUsers(fetchedSenders);
      }
    };
    const fetchReceivers = async () => {
      if (transactions) {
        const fetchedReceivers = await Promise.all(
          transactions.map((transaction) =>
            retrieveUser(transaction.receiving_user)
          )
        );
        setReceivingUsers(fetchedReceivers);
      }
    };

    fetchSenders();
    fetchReceivers();
  }, [transactions]);

  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setPage(value);
  };

  return (
    <Paper
      elevation={2}
      sx={{
        height: "100%",
        padding: "40px",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
      }}
    >
      <Box
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        {transactions?.map((transaction, index) => (
          <Box key={transaction.id}>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                borderBottom: "1px gray solid",
                alignItems: "center",
              }}
            >
              <Box sx={{ display: "flex", gap: "30px", alignItems: "center" }}>
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                  }}
                >
                  <Typography sx={{ fontWeight: 700, lineHeight: 1 }}>
                    {formatDateTime(transaction.created).day}
                  </Typography>
                  <Typography sx={{ lineHeight: 1 }}>
                    {formatDateTime(transaction.created).month}
                  </Typography>
                </Box>
                {React.cloneElement(
                  spendingIcons[transaction.spending_category_id - 1],
                  {
                    style: {
                      color:
                        receivingUsers[index]?.username != username
                          ? "IndianRed"
                          : "OliveDrab",
                    },
                  }
                )}
                <Typography sx={{ fontWeight: 700 }}>
                  {receivingUsers[index]?.username != username
                    ? receivingUsers[index]?.f_name
                    : sendingUsers[index]?.f_name}
                </Typography>
              </Box>
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-end",
                }}
              >
                <Typography>{transaction.detail}</Typography>
                {receivingUsers[index]?.username == username ? (
                  <Typography sx={{ fontWeight: 700, lineHeight: 1 }}>
                    {transaction.amount.toFixed(2)} {transaction.currency}
                  </Typography>
                ) : (
                  <Typography sx={{ fontWeight: 700, lineHeight: 1 }}>
                    - {transaction.amount.toFixed(2)} {transaction.currency}
                  </Typography>
                )}
              </Box>
            </Box>
          </Box>
        ))}
      </Box>
      {pageNumber !== 1 && (
        <Pagination
          count={pageNumber}
          page={page}
          variant="outlined"
          shape="rounded"
          sx={{ display: "flex", justifyContent: "center" }}
          onChange={handlePageChange}
        />
      )}
    </Paper>
  );
}

export default TransactionHistory;
