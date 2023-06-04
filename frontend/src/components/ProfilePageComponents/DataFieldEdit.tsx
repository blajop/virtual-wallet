import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import AccountCircle from "@mui/icons-material/AccountCircle";
import DoneIcon from "@mui/icons-material/Done";
import { useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import AlternateEmailIcon from "@mui/icons-material/AlternateEmail";
import LocalPhoneIcon from "@mui/icons-material/LocalPhone";
import Tooltip from "@mui/material/Tooltip/Tooltip";

type editDataState = [boolean, (e: boolean) => boolean];
type dataState = [string, (e: string) => string];

interface Props {
  data: dataState;
  editData: editDataState;
  label: string;
  icon: "name" | "email" | "phone";
  alert: boolean;
  alertMsg: string;
}

export default function EditProfile(props: Props) {
  const [editData, setEditData] = props.editData;
  const [data, setData] = props.data;
  const label = props.label;
  const icon = props.icon;
  const alert = props.alert;
  const alertMsg = props.alertMsg;

  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTextFieldValue(event.target.value);
  };

  const [textFieldValue, setTextFieldValue] = useState("");

  return (
    <Box
      sx={{
        "& > :not(style)": { m: 1 },
        display: "flex",
        alignItems: "center",
      }}
    >
      <TextField
        id="input-textfield"
        sx={{ width: "100%" }}
        value={textFieldValue}
        label={alert && !editData ? alertMsg : label}
        disabled={!editData}
        error={!editData && alert}
        onChange={handleInput}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              {icon === "name" && <AccountCircle sx={{ mr: "10px" }} />}
              {icon === "email" && <AlternateEmailIcon sx={{ mr: "10px" }} />}
              {icon === "phone" && <LocalPhoneIcon sx={{ mr: "10px" }} />}
              {!editData ? data : null}
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              {!editData ? (
                <Tooltip title="Edit">
                  <EditIcon
                    onClick={() => {
                      setEditData(true);
                    }}
                  ></EditIcon>
                </Tooltip>
              ) : (
                <Tooltip title="Accept">
                  <DoneIcon
                    onClick={() => {
                      setEditData(false);
                      if (textFieldValue != "") {
                        setData(textFieldValue);
                      }
                      setTextFieldValue("");
                    }}
                  />
                </Tooltip>
              )}
            </InputAdornment>
          ),
        }}
        variant="standard"
      />
    </Box>
  );
}
