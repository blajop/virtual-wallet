import React from "react";
import logo from "../assets/logo.png";

interface LogoProps {
  size: string;
}

const Logo: React.FC<LogoProps> = ({ size }) => {
  return <img src={logo} className={size} />;
};

export default Logo;
