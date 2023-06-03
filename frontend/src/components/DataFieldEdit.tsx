import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import AccountCircle from "@mui/icons-material/AccountCircle";
import DoneIcon from "@mui/icons-material/Done";
import { useState } from "react";
import EditIcon from "@mui/icons-material/Edit";

type editDataState = [boolean, (e: boolean) => boolean];
type dataState = [string, (e: string) => string];

interface Props {
  data: dataState;
  editData: editDataState;
  label: string;
}

export default function EditProfile(props: Props) {
  const [editData, setEditData] = props.editData;
  const [data, setData] = props.data;
  const label = props.label;

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
        value={textFieldValue}
        label={label}
        disabled={!editData}
        onChange={handleInput}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <AccountCircle />
              {!editData ? data : null}
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              {!editData ? (
                <EditIcon
                  onClick={() => {
                    setEditData(true);
                  }}
                ></EditIcon>
              ) : (
                <DoneIcon
                  onClick={() => {
                    setEditData(false);
                    setData(textFieldValue);
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
  );
}
