import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { baseUrl } from "../shared.js";
import axios from "axios";
import { useState } from "react";
import DataFieldEdit from "./DataFieldEdit.tsx";
import useDebounce from "../hooks/useDebounce.tsx";
import useValidateEmail from "../hooks/useValidateEmail.tsx";
import useValidatePhone from "../hooks/useValidatePhone.tsx";

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

export default function EditProfile(props: Props) {
  const [firstName, setFirstName] = useState(props.firstName);
  const [lastName, setLastName] = useState(props.lastName);
  const [email, setEmail] = useState(props.email);
  const [phone, setPhone] = useState(props.phone);

  const [editFirstName, setEditFirstName] = useState(false);
  const [editLastName, setEditLastName] = useState(false);
  const [editEmail, setEditEmail] = useState(false);
  const [editPhone, setEditPhone] = useState(false);
  const [editPwd, setEditPwd] = useState(false);

  const setEdit = [
    setEditFirstName,
    setEditLastName,
    setEditEmail,
    setEditPhone,
  ];

  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setOpen(true);
    for (const el of setEdit) {
      el(false);
    }
    setFirstName(props.firstName);
    setLastName(props.lastName);
    setEmail(props.email);
    setPhone(props.phone);
  };

  const handleClose = () => setOpen(false);

  const [alertEmail, setAlertEmail] = useState(false);
  const [alertMsgEmail, setAlertMsgEmail] = useState("");

  // CUSTOM HOOK EMAIL
  const debouncedEmail = useDebounce(email, 0);

  useValidateEmail(
    debouncedEmail,
    [
      alertEmail,
      (value: boolean) => {
        setAlertEmail(value);
        return value;
      },
    ],
    [
      alertMsgEmail,
      (value: string) => {
        setAlertMsgEmail(value);
        return value;
      },
    ]
  );

  const [alertPhone, setAlertPhone] = useState(false);
  const [alertMsgPhone, setAlertMsgPhone] = useState("");

  // CUSTOM HOOK PHONE
  const debouncedPhone = useDebounce(phone, 0);

  useValidatePhone(
    debouncedPhone,
    [
      alertPhone,
      (value: boolean) => {
        setAlertPhone(value);
        return value;
      },
    ],
    [
      alertMsgPhone,
      (value: string) => {
        setAlertMsgPhone(value);
        return value;
      },
    ]
  );

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
              icon="name"
              alert={false}
              alertMsg={""}
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
              icon="name"
              alert={false}
              alertMsg={""}
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
              icon="email"
              alert={email != props.email ? alertEmail : false}
              alertMsg={email != props.email ? alertMsgEmail : ""}
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
              icon="phone"
              alert={phone != props.phone ? alertPhone : false}
              alertMsg={phone != props.phone ? alertMsgPhone : ""}
            ></DataFieldEdit>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
