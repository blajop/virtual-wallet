import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Logo from "../components/Logo";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

export default function Overview() {
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
        id="back-to-top-anchor"
        maxWidth={"lg"}
        className="pt-60 snap-start "
        sx={{
          display: "flex",
          justifyContent: "center",
          scrollSnapAlign: "start",
          height: "calc(100vh - 64px)",
        }}
      >
        <Box
          component="div"
          sx={{
            display: "inline-block",
            width: "fit-content",
          }}
        >
          <Logo size={"h-[6rem]"} />
          <Typography
            variant="h6"
            sx={{ letterSpacing: 0.6 }}
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
            }}
          >
            <Button
              // variant="outlined"
              size="small"
              onClick={handleScrollToFeatures}
              sx={{
                borderColor: "black",
                color: "black",
                paddingX: "2rem",
                textTransform: "none",
                "&:hover": {
                  borderColor: "black",
                  textDecoration: "underline",
                  backgroundColor: "white",
                },
              }}
            >
              <strong>Learn more</strong>
            </Button>
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
          </Box>
        </Box>
      </Container>
    </>
  );
}
