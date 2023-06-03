import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { baseUrl } from "../shared.js";
import axios from "axios";
import Paper from "@mui/material/Paper";
import { useRef, useState } from "react";
import DataFieldEdit from "./DataFieldEdit.tsx";

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

  const [firstName, setFirstName] = useState(props.firstName);
  const [lastName, setLastName] = useState(props.lastName);
  const [email, setEmail] = useState(props.email);
  const [phone, setPhone] = useState(props.phone);

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
            <DataFieldEdit
              data={[
                firstName,
                (value: string) => {
                  setFirstName(value);
                  return value;
                },
              ]}
              editData={[
                editFirstName,
                (value: boolean) => {
                  setEditFirstName(value);
                  return value;
                },
              ]}
              label="First Name"
            ></DataFieldEdit>
            <DataFieldEdit
              data={[
                lastName,
                (value: string) => {
                  setLastName(value);
                  return value;
                },
              ]}
              editData={[
                editLastName,
                (value: boolean) => {
                  setEditLastName(value);
                  return value;
                },
              ]}
              label="Last Name"
            ></DataFieldEdit>
            <DataFieldEdit
              data={[
                email,
                (value: string) => {
                  setEmail(value);
                  return value;
                },
              ]}
              editData={[
                editEmail,
                (value: boolean) => {
                  setEditEmail(value);
                  return value;
                },
              ]}
              label="Email"
            ></DataFieldEdit>
            <DataFieldEdit
              data={[
                phone,
                (value: string) => {
                  setPhone(value);
                  return value;
                },
              ]}
              editData={[
                editPhone,
                (value: boolean) => {
                  setEditPhone(value);
                  return value;
                },
              ]}
              label="Phone"
            ></DataFieldEdit>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
