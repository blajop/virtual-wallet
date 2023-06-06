import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { baseUrl } from "../../shared.js";
import axios from "axios";
import { useEffect, useState } from "react";
import DataFieldEdit from "./DataFieldEdit.tsx";
import useValidateEmail from "../../hooks/useValidateEmail.tsx";
import useValidatePhone from "../../hooks/useValidatePhone.tsx";
import ButtonBlack from "../Buttons/ButtonBlack.tsx";
import Tooltip from "@mui/material/Tooltip/Tooltip";
import ModalPass from "./ModalPass.tsx";

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

type dataState = [string, (e: string) => string];

interface Props {
  firstName: dataState;
  lastName: dataState;
  username: string;
  email: dataState;
  phone: dataState;
}

export default function EditProfile(props: Props) {
  const [, setFirstName] = props.firstName;
  const [, setLastName] = props.lastName;
  const username = props.username;
  const [email, setEmail] = props.email;
  const [phone, setPhone] = props.phone;

  const [tempFirstName, setTempFirstName] = useState(props.firstName[0]);
  const [tempLastName, setTempLastName] = useState(props.lastName[0]);
  const [tempEmail, setTempEmail] = useState(props.email[0]);
  const [tempPhone, setTempPhone] = useState(props.phone[0]);

  const [editFirstName, setEditFirstName] = useState(false);
  const [editLastName, setEditLastName] = useState(false);
  const [editEmail, setEditEmail] = useState(false);
  const [editPhone, setEditPhone] = useState(false);

  // const [, setPwd] = useState("");
  // const [editPwd, setEditPwd] = useState(false);

  const setEdit = [
    setEditFirstName,
    setEditLastName,
    setEditEmail,
    setEditPhone,
  ];

  const [alertEmail, setAlertEmail] = useState(false);
  const [alertMsgEmail, setAlertMsgEmail] = useState("");

  const [alertPhone, setAlertPhone] = useState(false);
  const [alertMsgPhone, setAlertMsgPhone] = useState("");

  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
    for (const el of setEdit) {
      el(false);
    }
    setTempFirstName(props.firstName[0]);
    setTempLastName(props.lastName[0]);
    setTempEmail(props.email[0]);
    setTempPhone(props.phone[0]);
  };

  const handleClose = () => setOpen(false);

  // CUSTOM HOOK EMAIL

  useValidateEmail(
    tempEmail,
    [
      alertEmail,
      (value: boolean) => {
        if (email != tempEmail) {
          setAlertEmail(value);
          return value;
        } else {
          setAlertEmail(false);
          return value;
        }
      },
    ],
    [
      alertMsgEmail,
      (value: string) => {
        if (email != tempEmail) {
          setAlertMsgEmail(value);
          return value;
        } else {
          setAlertMsgEmail("");
          return value;
        }
      },
    ]
  );

  // CUSTOM HOOK PHONE

  useValidatePhone(
    tempPhone,
    [
      alertPhone,
      (value: boolean) => {
        if (phone != tempPhone) {
          setAlertPhone(value);
          return value;
        } else {
          setAlertPhone(false);
          return value;
        }
      },
    ],
    [
      alertMsgPhone,
      (value: string) => {
        if (phone != tempPhone) {
          setAlertMsgPhone(value);
          return value;
        } else {
          setAlertMsgPhone("");
          return value;
        }
      },
    ]
  );

  const [canSubmit, setCanSubmit] = useState(true);

  useEffect(() => {
    const conditions = [
      alertEmail,
      alertPhone,
      editFirstName,
      editLastName,
      editEmail,
      editPhone,
    ];
    if (conditions.every((element) => element === false)) {
      setCanSubmit(true);
    } else {
      setCanSubmit(false);
    }
  }, [
    alertEmail,
    alertPhone,
    editFirstName,
    editLastName,
    editEmail,
    editPhone,
  ]);

  const handleApply = () => {
    setFirstName(tempFirstName);
    setLastName(tempLastName);
    setEmail(tempEmail);
    setPhone(tempPhone);

    const finalData = {
      f_name: tempFirstName,
      l_name: tempLastName,
      email: tempEmail,
      phone: tempPhone,
    };
    axios
      .put(`${baseUrl}api/v1/users/profile`, finalData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          console.log(response);
        }
      })
      .catch();
    handleClose();
  };

  return (
    <div>
      <Tooltip title={"Edit profile"}>
        <Button onClick={handleOpen}>
          <EditIcon fontSize="large" sx={{ color: "black" }} />
        </Button>
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
            <DataFieldEdit
              data={[
                tempFirstName,
                (value: string) => {
                  setTempFirstName(value);
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
                tempLastName,
                (value: string) => {
                  setTempLastName(value);
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
                tempEmail,
                (value: string) => {
                  setTempEmail(value);
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
              alert={alertEmail}
              alertMsg={alertMsgEmail}
            ></DataFieldEdit>
            <DataFieldEdit
              data={[
                tempPhone,
                (value: string) => {
                  setTempPhone(value);
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
              alert={alertPhone}
              alertMsg={alertMsgPhone}
            ></DataFieldEdit>
            <ModalPass username={username}></ModalPass>
            <ButtonBlack
              size="medium"
              onClick={handleApply}
              disabled={!canSubmit}
              disabledText="Please fill in correct data"
            >
              Apply
            </ButtonBlack>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
