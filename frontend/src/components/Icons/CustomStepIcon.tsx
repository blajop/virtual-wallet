import {
  StepIconProps,
  StepIcon,
  StepLabel,
  Stepper,
  Typography,
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";

interface CustomStepIconProps extends StepIconProps {
  active: boolean;
  completed: boolean;
}

const CustomStepIcon = (props: CustomStepIconProps) => {
  const { active, completed, ...rest } = props;
  const iconColor = active ? "black" : completed ? "black" : "default";

  return (
    <StepIcon {...rest} completed={completed} active={active}>
      {completed ? (
        <CheckIcon style={{ color: "black" }} />
      ) : (
        <div
          style={{
            color: iconColor,
            width: 24,
            height: 24,
            border: `1px solid ${iconColor}`,
            borderRadius: "50%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {props.icon}
        </div>
      )}
    </StepIcon>
  );
};
export default CustomStepIcon;
