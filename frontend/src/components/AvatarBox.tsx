import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";

export default function AvatarBox({ image, name }) {
  return (
    <>
      <Box
        component="div"
        sx={{
          display: "inline-block",
          width: "fit-content",
        }}
      >
        {" "}
        <Box sx={{ width: "fit-content" }} className="flex flex-col text-left">
          <Box
            sx={{
              width: "150px",
              height: "150px",
              overflow: "hidden",
            }}
          >
            <Avatar
              variant="square"
              sx={{
                height: "auto",
                width: "auto",
                transition: "scale 0.1s ease-in-out",
                "&:hover": {
                  scale: "1.1",
                  textDecoration: "underline",
                  backgroundColor: "white",
                },
              }}
              src={image}
            ></Avatar>
          </Box>
          <Typography variant="body2" className="text-black font-bold pt-2">
            {name}
          </Typography>
        </Box>
      </Box>
    </>
  );
}
