import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import { apiUrl, baseUrl } from "../../shared.js";
import axios from "axios";
import { useEffect, useState } from "react";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";
import SendIcon from "@mui/icons-material/Send";
import SelectSmall from "../Select/Select.tsx";
import { Card, Wallet } from "../../pages/Profile.tsx";
import SelectCard from "../Select/SelectCard.tsx";
import LabelCheckbox from "../Icons/CheckboxRecurr.tsx";
import Checkbox from "@mui/material/Checkbox";
import { Select, Tooltip } from "@mui/material";
import Recurrence from "../Select/Recurrence.tsx";

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

interface Props {
  username: string | undefined;
  //   wallet: Wallet | undefined;
  //   card: Card | undefined;
}

export default function Transaction(props: Props) {
  const [wallet, setWallet] = useState<Wallet | undefined>();
  //   const [card, setCard] = useState<Card | undefined>();
  const username = props.username;

  // Transaction data
  const [recurringChecked, setRecurringChecked] = useState(false);
  const [recurrence, setRecurrence] = useState("");

  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
    setRecurringChecked(false);
  };
  const handleClose = () => setOpen(false);

  const handleSelectWallet = (wallet: Wallet | undefined) => {
    setWallet(wallet);
  };

  const selectRecurrence = (value: string) => {
    setRecurrence(value);
    return value;
  };

  useEffect(() => {
    if (recurringChecked === false) {
      setRecurrence("");
    }
  }, [recurringChecked]);

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
    <div>
      <Tooltip title="Send money">
        <SendIcon
          fontSize="medium"
          sx={{ color: "black", cursor: "pointer" }}
          onClick={handleOpen}
        />
      </Tooltip>
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
        <Fade in={open}>
          <Box sx={style}>
            <SelectSmall username={username!} setWallet={handleSelectWallet} />
            <LabelCheckbox
              isChecked={[
                recurringChecked,
                (value: boolean) => {
                  setRecurringChecked(value);
                  return value;
                },
              ]}
            />
            {recurringChecked && (
              <Recurrence
                recurrence={[recurrence, selectRecurrence]}
              ></Recurrence>
            )}
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
