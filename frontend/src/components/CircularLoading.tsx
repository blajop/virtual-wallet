import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";

export default function CircularLoading() {
  return (
    <Box
      sx={{
        position: "absolute",
        top: "60px",
        left: 0,
        width: "100%",
        height: "calc(100% - 60px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "rgba(255, 255, 255, 1)",
        zIndex: 9999,
      }}
    >
      <CircularProgress
        sx={{
          color: "black",
        }}
      />
    </Box>
  );
}
