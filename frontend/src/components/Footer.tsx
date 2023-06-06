import Box from "@mui/material/Box/Box";
import fastapi from "../assets/logos/fastapi.png";
import mariadb from "../assets/logos/mariadb.png";
import typescript from "../assets/logos/typescript.png";
import vite from "../assets/logos/vite.png";
import react from "../assets/logos/react.png";
import Tooltip from "@mui/material/Tooltip/Tooltip";

export default function Footer() {
  return (
    <Box
      sx={{
        height: "80px",
        marginTop: "-80px",
        width: "100%",
        backgroundColor: "black",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "base",
          gap: "20px",
        }}
      >
        <Tooltip title="Vite">
          <img className="h-[30px]" src={vite} />
        </Tooltip>
        <Tooltip title="React">
          <img className="h-[30px]" src={react} />
        </Tooltip>

        <Tooltip title="TypeScript">
          <img className="h-[30px]" src={typescript} />
        </Tooltip>

        <Tooltip title="FastAPI">
          <img className="h-[30px]" src={fastapi} />
        </Tooltip>

        <Tooltip title="MariaDB">
          <img className="h-[30px]" src={mariadb} />
        </Tooltip>
      </Box>
    </Box>
  );
}
