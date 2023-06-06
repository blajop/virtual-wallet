import Box from "@mui/material/Box/Box";
import Card from "@mui/material/Card/Card";
import CardContent from "@mui/material/CardContent/CardContent";
import Paper from "@mui/material/Paper/Paper";
import Typography from "@mui/material/Typography/Typography";
import formatNumber from "../../functions/formatNumber";

function Cards({
  holder,
  number,
  exp,
}: {
  holder: string;
  number: string;
  exp: Date;
}) {
  const options = { month: "2-digit" as const, year: "2-digit" as const };
  const formattedDate = exp.toLocaleDateString("en-US", options);

  const formattedNumber = formatNumber(number);
  return (
    <Card
      sx={{
        minWidth: 500,
        padding: "1rem",
        backgroundColor: "white",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <CardContent>
        <Paper
          sx={{
            width: "344px",
            height: " 186px",
            borderRadius: "10px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "white",
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "end",
            }}
          >
            <Typography
              textAlign={"center"}
              sx={{
                fontSize: "20px",
                fontWeight: "700",
                letterSpacing: "2px",
              }}
            >
              {formattedNumber}
            </Typography>
            <Box
              sx={{
                marginTop: "10px",
                display: "flex",
                alignItems: "flex-end",
                flexDirection: "column",
              }}
            >
              <Typography sx={{ fontSize: "14px" }}>
                EXP {formattedDate}
              </Typography>
              <Typography sx={{ fontWeight: 700, letterSpacing: "1px" }}>
                {holder.toUpperCase()}
              </Typography>
            </Box>
          </Box>
        </Paper>
      </CardContent>
    </Card>
  );
}

export default Cards;
