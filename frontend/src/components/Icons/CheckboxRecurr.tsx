import * as React from "react";
import Checkbox from "@mui/material/Checkbox";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";

type dataState = [boolean, (e: boolean) => boolean];

interface Props {
  isChecked: dataState;
}

export default function LabelCheckbox(props: Props) {
  const [isChecked, setIsChecked] = props.isChecked;

  const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsChecked(event.target.checked);
  };

  return (
    <FormGroup aria-label="position" row>
      <FormControlLabel
        value="end"
        control={
          <Checkbox checked={isChecked} onChange={handleCheckboxChange} />
        }
        label="Recurring transaction"
        labelPlacement="end"
      />
    </FormGroup>
  );
}
