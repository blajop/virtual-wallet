import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

type dataState = [string, (e: string) => string];

interface Props {
  recurrence: dataState;
}

export default function Recurrence(props: Props) {
  const [recurrence, setRecurrence] = props.recurrence;
  const recurrOptions = ["month", "year"];

  const handleChange = (event: SelectChangeEvent) => {
    setRecurrence(event.target.value);
  };

  return (
    <FormControl sx={{ minWidth: 120, width: "100%" }}>
      <InputLabel id="demo-simple-select-helper-label">Recurrence</InputLabel>
      <Select
        labelId="demo-simple-select-helper-label"
        id="demo-simple-select-helper"
        value={recurrence}
        label="Recurrence"
        onChange={handleChange}
      >
        {recurrOptions.map((option) => (
          <MenuItem value={option}>{option}</MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
