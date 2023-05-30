import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper/Paper";

const features = [
  {
    id: 1,
    text: "Send and receive money to anyone without minding the currency gap - exchange with <strong>no fees!</strong>",
  },
  {
    id: 2,
    text: "Create multiple virtual wallets under your account with support of 10 different currencies!",
  },
  {
    id: 3,
    text: "Create shared wallets with friends or family - giving pocket money to your kids or sharing bills has never been easier!",
  },
  { id: 4, text: "Refer a friend and you both receive $20!" },
];

export default function Features() {
  return (
    <>
      <Container
        maxWidth={"false"}
        id="features"
        className="bg-white  snap-start"
        sx={{
          display: "flex",
          justifyContent: "center",
          mixBlendMode: "difference",
          pt: "10rem",
          scrollSnapAlign: "start",
          height: "calc(100vh - 64px)",
        }}
      >
        <Box
          component="div"
          sx={{
            maxWidth: "md",
          }}
        >
          <Box
            maxWidth={"sm"}
            sx={{
              display: "flex",
              justifyContent: "center",
              gap: "1rem",
              mt: "2rem",
            }}
          >
            {1 ? (
              <Paper variant="outlined" elevation={0} className="p-10 ">
                <Typography
                  variant="h5"
                  sx={{ letterSpacing: 0.6 }}
                  className="text-black font-bold"
                >
                  {features[2].text}
                </Typography>
              </Paper>
            ) : null}
          </Box>
        </Box>
      </Container>
    </>
  );
}
