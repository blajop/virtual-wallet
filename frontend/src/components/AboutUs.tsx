import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import AvatarBox from "./AvatarBox";

export default function AboutUs() {
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
              style={{
                textDecoration: "underline",
              }}
              href="https://www.linkedin.com/in/pavlov-blagoy/"
              target="_blank"
              onMouseEnter={(e) => (e.target.style.fontStyle = "italic")}
              onMouseLeave={(e) => (e.target.style.fontStyle = "inherit")}
            >
              Blago
            </a>{" "}
            and{" "}
            <a
              style={{ textDecoration: "underline" }}
              target="_blank"
              href="https://www.linkedin.com/in/stanislav-milchev/"
              onMouseEnter={(e) => (e.target.style.fontStyle = "italic")}
              onMouseLeave={(e) => (e.target.style.fontStyle = "inherit")}
            >
              Stan
            </a>
            , and this is our final project for the Telerik Academy. This site
            is our first experiment outside of Python.{" "}
            <a
              style={{ textDecoration: "underline" }}
              href="mailto:pavlov_blago@yahoo.com,milchev.st@gmail.com"
              target="_blank"
              onMouseEnter={(e) => (e.target.style.fontStyle = "italic")}
              onMouseLeave={(e) => (e.target.style.fontStyle = "inherit")}
            >
              Contact us!
            </a>
          </Typography>
        </Box>
      </Container>
    </>
  );
}
