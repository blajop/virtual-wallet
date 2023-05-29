import Overview from "../components/Overview";
import Features from "../components/Features";
import Fab from "@mui/material/Fab/Fab";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import CssBaseline from "@mui/material/CssBaseline/CssBaseline";
import ScrollTop from "../components/ScrollTop";

export default function Home() {
  return (
    <>
      <CssBaseline />
      <div
        style={{ height: `calc(100vh - 64px)` }}
        className="wawa snap-mandatory snap-y overflow-y-scroll scroll-smooth"
      >
        <Overview></Overview>
        <Features></Features>
      </div>
      <ScrollTop>
        <Fab size="small" aria-label="scroll back to top">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
    </>
  );
}
