import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Logo from "../Logo";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { LoginContext } from "../../App";

export default function Overview() {
  const [loggedIn] = useContext(LoginContext);
  const navigate = useNavigate();
  const handleScrollToFeatures = () => {
    const scrollTarget = document.getElementById("features");
    if (scrollTarget) {
      scrollTarget.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <>
      <Container
        id="overview"
        maxWidth={"lg"}
        className="align-center snap-start "
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          scrollSnapAlign: "start",
          height: "calc(100vh - 60px)",
        }}
      >
        <Box
          component="div"
          sx={{
            display: "flex",
            flexDirection: "column",
            "@media (max-width: 600px)": {
              justifyContent: "center",
              paddingBottom: "80px",
            },
          }}
        >
          <Box
            sx={{
              display: "flex",
              height: "6rem",
              "@media (max-width: 600px)": {
                justifyContent: "center",
              },
            }}
          >
            <Logo size={"h-[6rem]"} />
          </Box>
          <Typography
            variant="h6"
            sx={{
              letterSpacing: 0.6,
              "@media (max-width: 600px)": {
                textAlign: "center",
              },
            }}
            className="text-black font-bold"
          >
            Join Uncle’s wallet and never worry about your spendings again.
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              gap: "1rem",
              mt: "2rem",
              "@media (max-width: 600px)": {
                justifyContent: "center",
                textAlign: "center",
              },
            }}
          >
            <Button
              variant={loggedIn ? "contained" : "text"}
              size="small"
              onClick={handleScrollToFeatures}
              sx={{
                borderColor: "black",
                color: !loggedIn ? "black" : "white",
                paddingX: "2rem",
                textTransform: "none",
                backgroundColor: loggedIn ? "black" : "transparent",

                "&:hover": {
                  borderColor: "black",
                  color: !loggedIn ? "black" : "unset",
                  textDecoration: loggedIn ? "unset" : "underline",
                  backgroundColor: "white",
                },
              }}
            >
              <strong>Learn more</strong>
            </Button>
            {loggedIn || (
              <Button
                variant="outlined"
                size="small"
                onClick={() => navigate("/register")}
                sx={{
                  paddingY: "0rem",
                  paddingX: "2rem",
                  color: "white",
                  backgroundColor: "black",
                  textTransform: "none",
                  "&:hover": {
                    backgroundColor: "white",
                    color: "black",
                    borderColor: "black",
                  },
                }}
              >
                <strong>Join now</strong>
              </Button>
            )}
          </Box>
        </Box>
      </Container>
    </>
  );
}
