import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import MenuItem from "@mui/material/MenuItem";
import { NavLink } from "react-router-dom";
import Logo from "./Logo";
import UserDropdown from "./UserDropdown";

const pages = [
  { name: "Overview", href: "/" },
  { name: "Features", href: "/register" },
  { name: "Contact us", href: "/" },
];

interface HeaderProps {
  children: React.ReactNode;
}

function Header(props: HeaderProps) {
  const [showLogo, setShowLogo] = React.useState<boolean>(true);

  React.useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      if (scrollPosition > 0) {
        setShowLogo(false);
      } else {
        setShowLogo(true);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
    null
  );

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  return (
    <>
      <AppBar
        position="sticky"
        sx={{
          boxShadow: "none",
          borderBottom: "solid 1px black",
          backgroundColor: "white",
          // mixBlendMode: "difference",
        }}
      >
        <Container maxWidth="lg">
          <Toolbar disableGutters>
            <Typography
              variant="h6"
              noWrap
              sx={{
                mr: 2,
                display: { xs: "none", md: "flex" },
                fontFamily: "Helvetica",
                fontWeight: 700,
                letterSpacing: ".3rem",
                color: "inherit",
                textDecoration: "none",
              }}
            >
              <NavLink
                to="/"
                style={{ textDecoration: "none", color: "white" }}
              >
                {showLogo ? (
                  <Logo
                    size={"h-[2rem] top-[1rem] invert mix-blend-difference"}
                  />
                ) : (
                  <>
                    <Logo size={"h-[2rem] top-[1rem]  mix-blend-difference"} />
                    <Logo
                      size={
                        "h-[2rem] top-[1rem] fixed invert mix-blend-difference"
                      }
                    />
                  </>
                )}
              </NavLink>
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
              <Menu
                className="pl-2"
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "left",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "left",
                }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{
                  display: { xs: "block", md: "none" },
                }}
              >
                {pages.map((page) => (
                  <MenuItem key={page.name} onClick={handleCloseNavMenu}>
                    <Typography textAlign="center">{page.name}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>
            <Typography
              variant="h5"
              noWrap
              sx={{
                mr: 2,
                display: { xs: "flex", md: "none" },
                flexGrow: 1,
                fontFamily: "Helvetica",
                fontWeight: 700,
                letterSpacing: ".3rem",
                color: "inherit",
                textDecoration: "none",
              }}
            >
              <NavLink key="logo" to="/">
                <Logo size={"h-[2rem]"} />
              </NavLink>
            </Typography>
            <Box
              className="justify-center"
              sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}
            >
              {pages.map((page) => (
                <NavLink
                  key={page.name}
                  to={page.href}
                  // to="#features"
                  onClick={handleCloseNavMenu}
                  className="font-helvetica font-medium  text-xl my-1 mx-10 text-black block"
                >
                  {page.name}
                </NavLink>
              ))}
            </Box>
            {false ? (
              <UserDropdown />
            ) : (
              <NavLink
                key="login"
                to="/login"
                className="font-helvetica font-medium text-xl my-1 mx-10 text-black block"
              >
                Login
              </NavLink>
            )}
          </Toolbar>
        </Container>
      </AppBar>
      {props.children}
    </>
  );
}
export default Header;
