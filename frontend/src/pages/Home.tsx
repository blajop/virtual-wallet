import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Logo from "../components/Logo";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  return (
    <>
      <Container
        maxWidth={"lg"}
        className="mt-60 h-screen "
        sx={{
          display: "flex",
          justifyContent: "center",
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
