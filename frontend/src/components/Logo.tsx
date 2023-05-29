import React from "react";

interface LogoProps {
  size: string;
}

const Logo: React.FC<LogoProps> = ({ size }) => {
  return <img src="../src/assets/logo.png" className={size} />;
};

export default Logo;
