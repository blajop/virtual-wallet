import Carousel from "react-bootstrap/Carousel";
import Typography from "@mui/material/Typography";
import "bootstrap/dist/css/bootstrap.min.css";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import Box from "@mui/material/Box";
import { useState, useEffect } from "react";

type Item = {
  id: number;
  text: React.ReactNode;
};

function UncontrolledExample({ items }: { items: Item[] }) {
  const [index, setIndex] = useState(1);
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  const [isMediumScreen, setIsMediumScreen] = useState(false);
  const [isWideScreen, setIsWideScreen] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const windowWidth = window.innerWidth;
      setIsSmallScreen(windowWidth <= 600); // Adjust the breakpoint as needed
      setIsMediumScreen(windowWidth > 600 && windowWidth <= 900); // Adjust the breakpoint as needed
      setIsWideScreen(windowWidth > 900); // Adjust the breakpoint as needed
    };

    handleResize(); // Check screen size on initial render

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const handleSelect = (selectedIndex: number) => {
    setIndex(selectedIndex);
  };

  return (
    <Carousel
      activeIndex={index}
      onSelect={handleSelect}
      prevIcon={<ArrowBackIosIcon sx={{ color: "black" }} />}
      nextIcon={<ArrowForwardIosIcon sx={{ color: "black" }} />}
    >
      {items.map((item) => (
        <Carousel.Item key={item.id}>
          <Box
            className={`mx-20 ${
              isWideScreen ? "px-[200px]" : isMediumScreen ? "px-[50px]" : ""
            } flex items-center  h-[500px]`}
            style={
              index === item.id ? { height: "500px", display: "flex" } : {}
            }
          >
            <Typography
              textAlign="center"
              variant={isSmallScreen ? "h6" : isMediumScreen ? "h4" : "h3"}
              sx={{ letterSpacing: 0.6 }}
              className="text-black font-bold"
            >
              {item.text}
            </Typography>
          </Box>
        </Carousel.Item>
      ))}
    </Carousel>
  );
}

export default UncontrolledExample;
