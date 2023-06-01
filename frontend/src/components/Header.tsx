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
import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";
import Logo from "./Logo";
import UserDropdown from "./UserDropdown";
import { LoginContext } from "../App";
import CircularLoading from "./CircularLoading";

const pages = [
  { name: "Overview", href: "overview" },
  { name: "Features", href: "features" },
  { name: "Contact us", href: "contact" },
];

interface HeaderProps {
  children: React.ReactNode;
}

function Header(props: HeaderProps) {
  const [showLogo, setShowLogo] = React.useState<boolean>(true);
  const [loggedIn, setLoggedIn] = React.useContext(LoginContext);
  const [loading, setLoading] = React.useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
    null
  );

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleLinkClick = (
    event: React.MouseEvent<HTMLElement>,
    elem: string
  ) => {
    const isHomePage = location.pathname === "/";
    handleCloseNavMenu();
    event.preventDefault();

    if (!isHomePage) {
      setLoading(true);
      navigate(`/`);
      setTimeout(() => {
        const scrollTarget = document.getElementById(elem);
        if (scrollTarget) {
          scrollTarget.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
          setLoading(false);
          console.log("stopLoading");
        }
      }, 500);
    } else {
      const scrollTarget = document.getElementById(elem);
      if (scrollTarget) {
        scrollTarget.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }
  };

  return (
    <>
      <AppBar
        position="static"
        sx={{
          boxShadow: "none",
          backgroundColor: "black",
          height: "60px",
          alignContent: "center !important",
        }}
      >
        <Container
          maxWidth="lg"
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            height: "60px",
            alignContent: "center ",
          }}
        >
          {/* LOGO ON WIDE SCREEN */}
          <Typography
            variant="h6"
            noWrap
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "Helvetica",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "white",
              textDecoration: "none",
            }}
          >
            <Link
              key={"overview"}
              to={"overview"}
              onClick={(e) => handleLinkClick(e, "overview")}
              style={{ textDecoration: "none", color: "white" }}
            >
              <Logo size={"h-[2rem] top-[1rem] invert mix-blend-difference"} />
            </Link>
          </Typography>

          <Toolbar
            disableGutters
            sx={{ display: "flex", justifyContent: "space-between" }}
          >
            {/* HAMBURGER MENU ON SMALL SCREEN */}
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
            {/* MENUS ON WIDE SCREEN */}
            <Box
              className="justify-center"
              sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}
            >
              {pages.map((page) => (
                <Link
                  key={page.name}
                  to={page.href}
                  onClick={(e) => handleLinkClick(e, page.href)}
                  className="font-helvetica font-medium  text-xl my-1 mx-10 text-white block"
                >
                  {page.name}
                </Link>
              ))}
            </Box>
          </Toolbar>
          {/* LOGO ON SMALL SCREEN */}
          <Typography
            variant="h5"
            noWrap
            sx={{
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontFamily: "Helvetica",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "white",
              textDecoration: "none",
              justifyContent: "center",
            }}
          >
            <NavLink key="logo" to="/">
              <Logo size={"h-[2rem] flex  invert"} />
            </NavLink>
          </Typography>
          {/* LOGIN OR USER MENU */}
          {loggedIn ? (
            <UserDropdown />
          ) : (
            <NavLink key="login" to="/login">
              <Typography
                sx={{
                  width: "50px",
                  fontWeight: "500",
                  fontSize: "1.25rem",
                  lineHeight: "1.75rem",
                  "&:hover": {
                    color: "white",
                  },
                }}
              >
                Login
              </Typography>
            </NavLink>
          )}
        </Container>
      </AppBar>
      {loading && <CircularLoading />}
      {props.children}
    </>
  );
}
export default Header;
