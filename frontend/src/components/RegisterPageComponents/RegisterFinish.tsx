import Paper from "@mui/material/Paper/Paper";
import Typography from "@mui/material/Typography/Typography";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function RegisterFinish() {
  const [seconds, setSeconds] = useState(15);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      if (seconds > 0) {
        setSeconds((prevSeconds) => prevSeconds - 1);
      }
    }, 1000);

    return () => {
      if (seconds === 1) navigate("/");
      clearInterval(interval);
    };
  }, [seconds]);

  return (
    <Paper sx={{ width: "70%", mt: "40px", padding: "40px" }}>
      <Typography variant="h3" textAlign={"center"}>
        Welcome!
      </Typography>
      <Typography variant="h6" className="pt-2 pb-20" textAlign={"center"}>
        Your account is all set up! Check out your{" "}
        <a
          className="hover:cursor-pointer text-blue-700 "
          onClick={(e) => {
            e.preventDefault();
            navigate("/profile");
          }}
        >
          profile
        </a>{" "}
        where you can manage your wallets, cards and friends!
      </Typography>
      <Typography textAlign={"center"}>
        <strong>You will be redirected to the homepage in {seconds}</strong>
      </Typography>
    </Paper>
  );
}

export default RegisterFinish;
