import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import AvatarBox from "./AvatarBox";

export default function AboutUs() {
  const jumpEffectStyle = {
    textDecoration: "underline",
    textDecorationThickness: "1px",
    display: "inline-block",
    transition: "transform 0.2s ease-in-out",
    transform: "translateY(0)",
  };

  const handleMouseEnter = (e) => {
    // e.target.style.fontStyle = "italic";
    e.target.style.color = "black";
    e.target.style.transform = "translateY(-2px)";
  };

  const handleMouseLeave = (e) => {
    e.target.style.fontStyle = "inherit";
    e.target.style.transform = "translateY(0)";
  };
  return (
    <>
      <Container
        id="contact"
        maxWidth={"sm"}
        className="align-center snap-start "
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          scrollSnapAlign: "start",
          height: "calc(100vh - 60px)",
        }}
      >
        <Box className="flex gap-10">
          <AvatarBox image="./src/assets/images/blago.png"></AvatarBox>
          <AvatarBox image="./src/assets/images/stani.png"></AvatarBox>
        </Box>
        <Box className="mt-10">
          <Typography
            variant="h6"
            sx={{ letterSpacing: 0.6 }}
            className="text-black font-bold"
          >
            We are{" "}
            <a
              style={jumpEffectStyle}
              href="https://www.linkedin.com/in/pavlov-blagoy/"
              target="_blank"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              Blago
            </a>{" "}
            and{" "}
            <a
              style={jumpEffectStyle}
              target="_blank"
              href="https://www.linkedin.com/in/stanislav-milchev/"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              Stan
            </a>
            , and this is our final project for the Telerik Academy. This site
            is our first experiment outside of Python.{" "}
            <a
              className="jump-effect"
              style={jumpEffectStyle}
              href="mailto:pavlov_blago@yahoo.com,milchev.st@gmail.com"
              target="_blank"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              Contact us!
            </a>
          </Typography>
        </Box>
      </Container>
    </>
  );
}
