import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import React from "react";
import { LoginContext } from "../App";
import { useNavigate } from "react-router-dom";

const settings = [
  { name: "Profile", href: "profile" },
  { name: "Settings", href: "settings" },
  { name: "Logout", href: "#" },
];

export default function UserDropdown() {
  const navigate = useNavigate();

  const [loggedIn, setLoggedIn] = React.useContext(LoginContext);
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(
    null
  );
  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  return (
    <Box
      sx={{
        flexGrow: 0,
        width: "50px",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <Tooltip title="Open settings">
        <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
          <Avatar
            alt="avatar"
            sx={{ width: "32px", height: "32px" }}
            src={localStorage.getItem("avatar") ?? ""}
          />
        </IconButton>
      </Tooltip>
      <Menu
        sx={{ mt: "45px" }}
        id="menu-appbar"
        anchorEl={anchorElUser}
        anchorOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        keepMounted
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        open={Boolean(anchorElUser)}
        onClose={handleCloseUserMenu}
      >
        {settings.map((setting) => (
          <MenuItem
            key={setting.name}
            onClick={() => {
              if (setting.name === "Logout") {
                localStorage.removeItem("token");
                setLoggedIn(false);
                navigate("/");
              }
              handleCloseUserMenu;
              navigate(setting.href);
            }}
          >
            <Typography textAlign="center">{setting.name}</Typography>
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
}
