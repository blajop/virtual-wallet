import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import UncontrolledExample from "./Carousel";

const features = [
  {
    id: 1,
    text: (
      <p>
        Send and receive money to anyone without minding the currency gap -
        exchange with <strong>no fees!</strong>
      </p>
    ),
  },
  {
    id: 2,
    text: (
      <p>
        Create multiple virtual wallets under your account with support of 10
        different currencies!
      </p>
    ),
  },
  {
    id: 3,
    text: (
      <p>
        Share wallets with friends or family - giving pocket money to your kids
        or sharing bills has never been easier!
      </p>
    ),
  },
  { id: 4, text: <p>Invite friends and claim rewards!</p> },
];

export default function Features() {
  return (
    <>
      <Container
        maxWidth={"false"}
        id="features"
        className="bg-white "
        sx={{
          display: "flex",
          justifyContent: "center",
          alignContent: "center",
          mixBlendMode: "difference",
          scrollSnapAlign: "start",
          height: "calc(100vh - 60px)",
        }}
      >
        <Box
          maxWidth={"lg"}
          className={`wawa snap-mandatory snap-x overflow-y-scroll`}
          sx={{
            width: "lg",
            display: "flex",
            alignItems: "center",
            marginBottom: "60px",
          }}
        >
          <UncontrolledExample items={features} />{" "}
        </Box>
      </Container>
    </>
  );
}
