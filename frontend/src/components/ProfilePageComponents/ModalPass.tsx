import Button from "@mui/base/Button";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { useEffect, useState } from "react";
import KeyIcon from "@mui/icons-material/Key";
import ButtonBlack from "../Buttons/ButtonBlack";
import DataFieldEdit from "./DataFieldEdit";

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

export default function ModalPass() {
  const [oldPwd, setOldPwd] = useState("");
  const [newPwd, setNewPwd] = useState("");
  const [matchPwd, setMatchPwd] = useState("");

  const [editNewPwd, setEditNewPwd] = useState(false);
  const [editOldPwd, setEditOldPwd] = useState(false);
  const [editMatchPwd, setEditMatchPwd] = useState(false);

  const [open, setOpen] = useState(false);
  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = () => {
    setOpen(false);
  };

  // OLD PASS VERIFY
  // useEffect(() => {
  //   if (username !== "") {
  //     if (!USERNAME_REGEX.test(username)) {
  //       setAlertUsername(true);
  //       setAlertMsgUsername("Username should be [2,20] chars long");
  //     } else {
  //       setAlertUsername(false);
  //       setAlertMsgUsername("");

  //       axios
  //         .get(`${baseUrl}api/v1/username-unique/${username}`)
  //         .then((response) => {
  //           if (response.status === 200) {
  //             setAlertUsername(false);
  //             setAlertMsgUsername("");
  //           }
  //         })
  //         .catch(() => {
  //           setAlertUsername(true);
  //           setAlertMsgUsername("Username is already taken");
  //         });
  //     }
  //   } else {
  //     setAlertUsername(false);
  //     setAlertMsgUsername("");
  //   }
  // }, [username]);

  // CUSTOM HOOK PASSWORD
  //  useValidatePwd(
  //   password,
  //   [
  //     alertPwd,
  //     (value: boolean) => {
  //       setAlertPwd(value);
  //       return value;
  //     },
  //   ],
  //   [
  //     alertMsgPwd,
  //     (value: string) => {
  //       setAlertMsgPwd(value);
  //       return value;
  //     },
  //   ]
  // );

  // PASSWORD MATCH TEST
  // useEffect(() => {
  //   if (
  //     confirmPass != "" &&
  //     formReg["password"] != "" &&
  //     confirmPass != formReg["password"]
  //   ) {
  //     setalertConfirmPass(true);
  //   } else {
  //     setalertConfirmPass(false);
  //   }
  // }, [confirmPass, formReg["password"]]);

  const [canSubmit, setCanSubmit] = useState(true);

  // useEffect(() => {
  //   const conditions = [

  //   ];
  //   if (conditions.every((element) => element === false)) {
  //     setCanSubmit(true);
  //   } else {
  //     setCanSubmit(false);
  //   }
  // }, [

  // ]);

  return (
    <>
      <Button onClick={handleOpen}>
        <KeyIcon />
        Change Password
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="password-change"
        aria-describedby="password-change"
      >
        <Box sx={{ ...style, width: 300 }}>
          <DataFieldEdit
            data={[
              "",
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
            alert={false}
            alertMsg={""}
          ></DataFieldEdit>

          <DataFieldEdit
            data={[
              "",
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
            alert={false}
            alertMsg={""}
          ></DataFieldEdit>

          <DataFieldEdit
            data={[
              "",
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
            alert={false}
            alertMsg={""}
          ></DataFieldEdit>
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
