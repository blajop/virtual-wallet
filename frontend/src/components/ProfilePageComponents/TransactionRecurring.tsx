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
import TransactionRecurringDetail from "../Modals/TransactionRecurringDetail.tsx";

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

export function formatDateTime(
  dateTime: string,
  monthly?: boolean
): CustomDate {
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
  let month = "";
  {
    monthly
      ? (month = monthAbbreviations[date.getMonth() + 1])
      : (month = monthAbbreviations[date.getMonth()]);
  }

  return { day: day, month: month };
}

const spendingIcons = [
  <CreditCardIcon />,
  <LocalDiningIcon />,
  <LocalAtmIcon />,
];

function TransactionRecurring({ username }: { username: string }) {
  const [transactions, setTransactions] = useState<Transaction[]>();
  const [sendingUsers, setSendingUsers] = useState<User[]>([]);
  const [receivingUsers, setReceivingUsers] = useState<User[]>([]);

  const [detailedTransaction, setDetailedTransaction] = useState<Transaction>();
  const [open, setOpen] = useState<boolean>(false);

  const [page, setPage] = useState<number>(1);
  const [pageNumber, setPageNumber] = useState<number>();

  const handleDetailOpen = (value: boolean) => {
    setOpen(value);
  };

  useEffect(() => {
    axios
      .get(
        apiUrl +
          `transactions?recurring=True&direction=out&size=5&page=${page}`,
        {
          headers: { Authorization: `Bearer ${localStorage.token}` },
        }
      )
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
    event;
    setPage(value);
  };

  return (
    <Box
      sx={{
        padding: "40px",
        paddingY: "0px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        height: "100%",
      }}
    >
      {detailedTransaction && (
        <TransactionRecurringDetail
          username={username}
          open={[open, handleDetailOpen]}
          transaction={detailedTransaction}
        ></TransactionRecurringDetail>
      )}
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        {transactions?.map((transaction, index) => (
          <Box
            key={transaction.id}
            sx={{ cursor: "pointer" }}
            onClick={() => {
              setOpen(true);
              setDetailedTransaction(transaction);
            }}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                borderBottom: "1px lightgray solid",
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
                    {transaction.recurring === "Monthly"
                      ? formatDateTime(transaction.created, true).month
                      : formatDateTime(transaction.created).month}
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
                <Typography>
                  {transaction.recurring}: {transaction.detail}
                </Typography>
                <Typography sx={{ fontWeight: 700, lineHeight: 1 }}>
                  {transaction.amount.toFixed(2)} {transaction.currency}
                </Typography>
              </Box>
            </Box>
          </Box>
        ))}
      </Box>
      <Pagination
        count={pageNumber}
        page={page}
        variant="outlined"
        shape="rounded"
        sx={{ display: "flex", justifyContent: "center", marginTop: "20px" }}
        onChange={handlePageChange}
      />
    </Box>
  );
}

export default TransactionRecurring;
