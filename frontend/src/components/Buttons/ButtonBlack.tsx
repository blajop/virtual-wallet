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
  text: string | React.ReactNode;
}

export default function ButtonBlack(props: ButtonBlackProps) {
  const navigate = useNavigate();
  const {
    to = "#",
    size = "small",
    variant = "outlined",
    invert = false,
    text,
  } = props;

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
              borderColor: invert ? "black" : "white",
              "& .MuiSvgIcon-root": {
                color: invert ? "white" : "black",
              },
            },
          },
        },
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Button variant={variant} size={size} onClick={() => navigate(to)}>
        {text}
      </Button>
    </ThemeProvider>
  );
}
