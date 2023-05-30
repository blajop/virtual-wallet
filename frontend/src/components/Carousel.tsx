import Carousel from "react-bootstrap/Carousel";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import "bootstrap/dist/css/bootstrap.min.css";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import Box from "@mui/material/Box";
import { useState } from "react";

function UncontrolledExample({ items }) {
  const [index, setIndex] = useState(1);

  const handleSelect = (selectedIndex, e) => {
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
            className=" mx-20 px-[100px] flex items-center h-[500px]"
            style={
              index === item.id ? { height: "500px", display: "flex" } : {}
            }
          >
            <Typography
              textAlign={"center"}
              variant="h3"
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
