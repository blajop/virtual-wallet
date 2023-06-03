import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import EditIcon from "@mui/icons-material/Edit";
import { baseUrl } from "../shared.js";
import axios from "axios";
import Paper from "@mui/material/Paper";
import TxtField from "./TxtField.js";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import AccountCircle from "@mui/icons-material/AccountCircle";
import { useRef, useState } from "react";
import DoneIcon from "@mui/icons-material/Done";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  display: "flex",
  flexDirection: "column",
  gap: "10px",
};

interface Props {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
}

class UserData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  password: string;

  constructor(
    firstName: string = "",
    lastName: string = "",
    email: string = "",
    phone: string = "",
    password: string = ""
  ) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
    this.phone = phone;
    this.password = password;
  }
}

export default function EditProfile(props: Props) {
  const profile = new UserData(
    props.firstName,
    props.lastName,
    props.email,
    props.phone
  );

  const [editFirstName, setEditFirstName] = useState(false);
  const [editLastName, setEditLastName] = useState(false);
  const [editEmail, setEditEmail] = useState(false);
  const [editPhone, setEditPhone] = useState(false);
  const [editPwd, setEditPwd] = useState(false);

  const profileDetails = {
    firstName: profile.firstName,
    lastName: profile.lastName,
    email: profile.email,
    phone: profile.phone,
  };

  const [details, setDetails] = useState(profileDetails);

  const handleInput = (
    event: React.ChangeEvent<HTMLInputElement>,
    field: string
  ) => {
    setDetails({ ...details, [event.target.name]: event.target.value });
    if (event.target.name === field) {
      setTextFieldValue(event.target.value);
    }
  };

  const detailEdit = [editFirstName, editLastName, editEmail, editPhone];
  const setEdit = [
    setEditFirstName,
    setEditLastName,
    setEditEmail,
    setEditPhone,
  ];

  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setOpen(true);
    setDetails(profileDetails);
    for (const el of setEdit) {
      el(false);
    }
  };

  const handleClose = () => setOpen(false);
  const [textFieldValue, setTextFieldValue] = useState("");

  return (
    <div>
      <Button onClick={handleOpen}>
        <EditIcon />
      </Button>
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
            {Object.entries(details).map((entry, idx) => (
              <Box
                sx={{
                  "& > :not(style)": { m: 1 },
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <TextField
                  id="input-textfield"
                  name={entry[0]}
                  value={textFieldValue}
                  label={entry[0]}
                  disabled={!detailEdit[idx]}
                  onChange={(e) => {
                    handleInput(e, entry[0]);
                  }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <AccountCircle />
                        {!detailEdit[idx] ? entry[1] : null}
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        {!detailEdit[idx] ? (
                          <EditIcon
                            onClick={() => {
                              setEdit[idx](true);
                            }}
                          ></EditIcon>
                        ) : (
                          <DoneIcon
                            onClick={() => {
                              setEdit[idx](false);
                              setTextFieldValue("");
                            }}
                          />
                        )}
                      </InputAdornment>
                    ),
                  }}
                  variant="standard"
                />
              </Box>
            ))}
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
