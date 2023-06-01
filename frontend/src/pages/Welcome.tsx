import { useState } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Backdrop from "@mui/material/Backdrop";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { Slide } from "@mui/material";

const theme = createTheme({
  components: {
    MuiBackdrop: {
      styleOverrides: {
        root: {
          backgroundColor: "white",
        },
      },
    },
  },
});

const WelcomeScreen = () => {
  const [isVisible, setIsVisible] = useState(true);

  const handleDismiss = () => {
    setIsVisible(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <Backdrop
        open={isVisible}
        onClick={handleDismiss}
        TransitionComponent={Slide}
        transitionDuration={{ appear: 0, exit: 800, enter: 0 }}
        sx={{
          zIndex: 9999,
          transform: isVisible ? "translateY(0)" : undefined,
        }}
      >
        <Container sx={{ width: "auto", paddingBottom: "60px" }}>
          <Typography
            align="center"
            variant="h1"
            sx={{
              fontSize: "15rem",
              fontFamily: "Helvetica",
              fontWeight: 700,
              "@media (max-width: 600px)": {
                fontSize: "7rem",
              },
            }}
          >
            Hello!
          </Typography>
          <Typography
            align="center"
            variant="h6"
            sx={{
              fontSize: "2rem",
              fontWeight: 700,
              "@media (max-width: 600px)": {
                fontSize: "1.2rem",
              },
            }}
          >
            This is an educational project. Please do not enter any sensitive
            data! Enjoy!
          </Typography>
        </Container>
      </Backdrop>
    </ThemeProvider>
  );
};

export default WelcomeScreen;
