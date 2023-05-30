import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Logo from "../components/Logo";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import Avatar from "@mui/material/Avatar";
import AvatarBox from "./AvatarBox";

export default function AboutUs() {
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
        maxWidth={"sm"}
        className="align-center snap-start "
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          scrollSnapAlign: "start",
          height: "calc(100vh - 64px)",
        }}
      >
        <Box className="flex gap-10">
          <AvatarBox
            image="./src/assets/images/stani.png"
            name="Stan"
          ></AvatarBox>
          <AvatarBox
            image="./src/assets/images/blago.png"
            name="Blago"
          ></AvatarBox>
        </Box>
        <Box className="mt-10">
          <Typography
            variant="h6"
            sx={{ letterSpacing: 0.6 }}
            className="text-black font-bold"
          >
            We are Blago and Stan, and this is our final project for the Telerik
            Academy. This site is our first experiment outside of Python.
          </Typography>
        </Box>
      </Container>
    </>
  );
}
