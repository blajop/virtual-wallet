import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

type dataState = [string, (e: string) => string];

interface Props {
  selectable: dataState;
  options: string[];
  label: string;
  sx?: React.CSSProperties;
}

export default function SelectMisc(props: Props) {
  const [selectable, setSelectable] = props.selectable;
  const options = props.options;
  const label = props.label;
  const sx = props.sx;

  const handleChange = (event: SelectChangeEvent) => {
    setSelectable(event.target.value);
  };

  return (
    <FormControl sx={sx}>
      <InputLabel id="demo-simple-select-helper-label">{label}</InputLabel>
      <Select
        labelId="demo-simple-select-helper-label"
        id="demo-simple-select-helper"
        value={selectable}
        label={label}
        onChange={handleChange}
      >
        {options.map((option) => (
          <MenuItem value={option}>{option}</MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
