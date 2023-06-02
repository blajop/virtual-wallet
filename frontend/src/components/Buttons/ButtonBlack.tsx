import Button from "@mui/material/Button/Button";
import { useNavigate } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import React from "react";

interface ButtonBlackProps {
  to?: string;
  size?: "small" | "medium" | "large";
  variant?: "text" | "outlined" | "contained";
  invert?: boolean;
  leeches?: object[];
  text?: string;
  children?: React.ReactNode;
  onClick?: (to: string) => void;
  disabled?: boolean;
  disabledText?: string;
  sx?: object;
}

const ButtonBlack = React.forwardRef(function ButtonBlack(
  props: ButtonBlackProps
) {
  const navigate = useNavigate();
  const {
    to = "#",
    size = "small",
    variant = "outlined",
    invert = false,
    text,
    children,
    onClick,
    disabled,
    disabledText,
    sx,
  } = props;

  const handleClick = () => {
    if (onClick) {
      onClick(to);
    } else {
      navigate(to);
    }
  };

  const theme = createTheme({
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            paddingY: "0rem",
            paddingX: "2rem",
            color: invert ? "black" : "white",
            backgroundColor: invert ? "white" : "black",
            borderColor: !invert ? "white" : "black",
            textTransform: "none",
            "&:hover": {
              backgroundColor: invert ? "black" : "white",
              color: invert ? "white" : "black",
              borderColor: !invert ? "black" : "white",
              "& .MuiSvgIcon-root": {
                color: invert ? "white" : "black",
              },
            },
            "&.Mui-disabled": {
              border: "solid 1px black",
              color: "white",
              text: "Please fill the form",
            },
            "&.Mui-disabled:hover": {
              backgroundColor: invert ? "white" : "black",
              color: invert ? "white" : "black",
              borderColor: invert ? "black" : "white",
            },
          },
        },
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Button
        sx={sx}
        disabled={disabled}
        variant={variant}
        size={size}
        onClick={handleClick}
      >
        {disabled ? disabledText : children || text}
      </Button>
    </ThemeProvider>
  );
});

export default ButtonBlack;
