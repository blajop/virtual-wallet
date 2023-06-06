import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { useEffect, useState } from "react";
import ButtonBlack from "../Buttons/ButtonBlack";
import DataFieldEdit from "./DataFieldEdit";
import axios from "axios";
import { baseUrl } from "../../shared";
import useValidatePwd from "../../hooks/useValidatePwd";
import Snackbar from "@mui/material/Snackbar";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  pt: 2,
  px: 4,
  pb: 3,
};

interface Props {
  username: string;
}

export default function ChangePwd(props: Props) {
  const username = props.username;
  const [oldPwd, setOldPwd] = useState("");
  const [newPwd, setNewPwd] = useState("");
  const [matchPwd, setMatchPwd] = useState("");

  const [hiddenOldPwd, setHiddenOldPwd] = useState("");
  const [hiddenNewPwd, setHiddenNewPwd] = useState("");
  const [hiddenMatchPwd, setHiddenMatchPwd] = useState("");

  const [editNewPwd, setEditNewPwd] = useState(false);
  const [editOldPwd, setEditOldPwd] = useState(false);
  const [editMatchPwd, setEditMatchPwd] = useState(false);

  const [alertOldPwd, setAlertOldPwd] = useState(false);
  const [alertMsgOldPwd, setAlertMsgOldPwd] = useState("");
  const [alertNewPwd, setAlertNewPwd] = useState(false);
  const [alertMsgNewPwd, setAlertMsgNewPwd] = useState("");
  const [alertMatchPwd, setAlertMatchPwd] = useState(false);

  const [open, setOpen] = useState(false);
  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = () => {
    const finalData = {
      password: newPwd,
    };
    axios
      .put(`${baseUrl}api/v1/users/profile`, finalData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          console.log("successful pwd change");
        }
      })
      .catch();
    handleClose();
  };

  // HIDE PWDS

  useEffect(() => {
    setHiddenOldPwd("•".repeat(oldPwd.length));
    setHiddenNewPwd("•".repeat(newPwd.length));
    setHiddenMatchPwd("•".repeat(matchPwd.length));
  }, [oldPwd, newPwd, matchPwd]);

  // OLD PASS VERIFY
  useEffect(() => {
    if (oldPwd !== "") {
      const data = new URLSearchParams();
      data.append("username", username);
      data.append("password", oldPwd);

      axios
        .post(`${baseUrl}api/v1/login/access-token`, data, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        })
        .then((response) => {
          if (response.status === 200) {
            setAlertOldPwd(false);
            setAlertMsgOldPwd("");
          }
        })
        .catch(() => {
          setAlertOldPwd(true);
          setAlertMsgOldPwd("Incorrect old password");
        });
    }
  }, [oldPwd]);

  //  HOOK NEW PASSWORD
  useValidatePwd(
    newPwd,
    [
      alertNewPwd,
      (value: boolean) => {
        setAlertNewPwd(value);
        return value;
      },
    ],
    [
      alertMsgNewPwd,
      (value: string) => {
        setAlertMsgNewPwd(value);
        return value;
      },
    ]
  );

  // PASSWORD MATCH TEST
  useEffect(() => {
    if (matchPwd != "" && newPwd != "" && matchPwd != newPwd) {
      setAlertMatchPwd(true);
    } else {
      setAlertMatchPwd(false);
    }
  }, [matchPwd, newPwd]);

  const [canSubmit, setCanSubmit] = useState(true);

  // CAN SUBMIT TEST
  useEffect(() => {
    const conditions = [
      alertOldPwd,
      alertNewPwd,
      alertMatchPwd,
      editOldPwd,
      editNewPwd,
      editMatchPwd,
    ];
    const conditions2 = [oldPwd, newPwd, matchPwd];
    if (
      conditions.every((element) => element === false) &&
      conditions2.every((element) => element != "")
    ) {
      setCanSubmit(true);
    } else {
      setCanSubmit(false);
    }
  }, [
    alertOldPwd,
    alertNewPwd,
    alertMatchPwd,
    editOldPwd,
    editNewPwd,
    editMatchPwd,
    oldPwd,
    newPwd,
    matchPwd,
  ]);

  return (
    <>
      <ButtonBlack
        invert
        size="medium"
        sx={{ marginTop: "15px" }}
        onClick={handleOpen}
      >
        Change Password
      </ButtonBlack>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="password-change"
        aria-describedby="password-change"
      >
        <Box sx={{ ...style, width: 300 }}>
          <DataFieldEdit
            data={[
              hiddenOldPwd,
              (value: string) => {
                setOldPwd(value);
                return value;
              },
            ]}
            editData={[
              editOldPwd,
              (value: boolean) => {
                setEditOldPwd(value);
                return value;
              },
            ]}
            label="Old Password"
            icon="password"
            alert={alertOldPwd}
            alertMsg={alertMsgOldPwd}
          ></DataFieldEdit>

          <DataFieldEdit
            data={[
              hiddenNewPwd,
              (value: string) => {
                setNewPwd(value);
                return value;
              },
            ]}
            editData={[
              editNewPwd,
              (value: boolean) => {
                setEditNewPwd(value);
                return value;
              },
            ]}
            label="New Password"
            icon="password"
            alert={alertNewPwd}
            alertMsg="New Password"
          ></DataFieldEdit>

          <DataFieldEdit
            data={[
              hiddenMatchPwd,
              (value: string) => {
                setMatchPwd(value);
                return value;
              },
            ]}
            editData={[
              editMatchPwd,
              (value: boolean) => {
                setEditMatchPwd(value);
                return value;
              },
            ]}
            label="Confirm New Password"
            icon="password"
            alert={alertMatchPwd}
            alertMsg={"Passwords do not match"}
          ></DataFieldEdit>

          <Snackbar
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            open={alertNewPwd}
            // onClose={() => (alertNewPwd = false)}
            message={alertMsgNewPwd}
            key={"bottom" + "center"}
            ContentProps={{
              sx: {
                display: "flex",
                color: "white",
                fontWeight: "700",
                justifyContent: "center",
                backgroundColor: "black",
              },
            }}
          />
          <ButtonBlack
            size="medium"
            sx={{ width: "100%" }}
            onClick={handleConfirm}
            disabled={!canSubmit}
            disabledText="Please fill in correct data"
          >
            Confirm
          </ButtonBlack>
        </Box>
      </Modal>
    </>
  );
}
