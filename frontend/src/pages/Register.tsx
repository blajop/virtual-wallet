import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";
import Typography from "@mui/material/Typography";
import { Fragment, ReactNode, useState, useEffect } from "react";
import Register from "../components/Signup";
import axios, { AxiosError } from "axios";
import WalletCreate from "../components/WalletCreate";
import Container from "@mui/system/Container/Container";

const steps = ["New User", "Create Wallet", "Finish"];

export default function RegisterStepper() {
  const [alertUsername, setAlertUsername] = useState(false);
  const [alertEmail, setAlertEmail] = useState(false);
  const [alertPhone, setAlertPhone] = useState(false);
  const { formReg, alertConfirmPass, renderReg } = Register({
    alertUsername: alertUsername,
    alertEmail: alertEmail,
    alertPhone: alertPhone,
  });
  const username = formReg["username"];
  const email = formReg["email"];
  const phone = formReg["phone"];

  const [wallAlertMsg, setWallAlertMsg] = useState("");
  const { formWall, renderWall } = WalletCreate({
    wrongWallInputMsg: wallAlertMsg,
    f_name: formReg["f_name"],
    l_name: formReg["l_name"],
  });

  const pages = [renderReg, renderWall];
  const [activeStep, setActiveStep] = useState(0);
  const [activePage, setActivePage] = useState(0);

  useEffect(() => {
    if (username != "") {
      setTimeout(() => {
        axios
          .get(`http://localhost:8000/api/v1/username-unique/${username}`)
          .then((response) => {
            console.log(response.data);
            if (response.status === 200) {
              setAlertUsername(false);
            }
          })
          .catch((err: AxiosError) => {
            setAlertUsername(true);
          });
      }, 500);
    }
  }, [username]);

  useEffect(() => {
    if (email != "") {
      setTimeout(() => {
        axios
          .get(`http://localhost:8000/api/v1/email-unique/${email}`)
          .then((response) => {
            console.log(response.data);
            if (response.status === 200) {
              setAlertEmail(false);
            }
          })
          .catch((err: AxiosError) => {
            setAlertEmail(true);
          });
      }, 500);
    }
  }, [email]);

  useEffect(() => {
    if (phone != "") {
      setTimeout(() => {
        axios
          .get(`http://localhost:8000/api/v1/phone-unique/${phone}`)
          .then((response) => {
            console.log(response.data);
            if (response.status === 200) {
              setAlertPhone(false);
            }
          })
          .catch((err: AxiosError) => {
            setAlertPhone(true);
          });
      }, 500);
    }
  }, [phone]);

  // NEXT BUTTON HANDLER
  const handleNext = () => {
    if (activeStep === 0) {
      const conditions = [
        !alertConfirmPass,
        !alertUsername,
        !alertEmail,
        !alertPhone,
      ];
      const conditions2 = [
        formReg["f_name"],
        formReg["l_name"],
        formReg["username"],
        formReg["email"],
        formReg["phone"],
        formReg["password"],
      ];
      if (
        conditions.every((element) => element === true) &&
        conditions2.every((element) => element != "")
      ) {
        axios
          .post("http://localhost:8000/api/v1/signup", formReg)
          .then((response) => {
            if (response.status === 200) {
              setActiveStep((prevActiveStep) => prevActiveStep + 1);
              setActivePage((prevActivePage) => prevActivePage + 1);
            }
          })
          .catch((err: AxiosError) => console.log(err));
      }
    } else {
      setActiveStep((prevActiveStep) => prevActiveStep + 1);
      setActivePage((prevActivePage) => prevActivePage + 1);
    }
  };

  return (
    <Container
      maxWidth={"md"}
      className="pt-[100px]"
      sx={{ display: "flex", flexDirection: "column" }}
    >
      <Stepper activeStep={activeStep}>
        {steps.map((label) => {
          const stepProps: { completed?: boolean } = {};
          const labelProps: {
            optional?: ReactNode;
          } = {};
          return (
            <Step key={label} {...stepProps}>
              <StepLabel {...labelProps}>{label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>

      {activeStep === steps.length ? (
        <Fragment>
          <Typography sx={{ mt: 2, mb: 1 }}>You are all set!</Typography>
        </Fragment>
      ) : (
        <Fragment>
          {/* ACTIVE PAGE IS NESTED HERE BUTTON */}
          {pages[activePage]}
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              pt: 2,
            }}
          >
            {/* NEXT BUTTON */}
            <Button
              onClick={handleNext}
              variant="outlined"
              size="large"
              sx={{
                paddingY: "0rem",
                paddingX: "6rem",
                color: "white",
                backgroundColor: "black",
                textTransform: "none",
                "&:hover": {
                  backgroundColor: "white",
                  color: "black",
                  borderColor: "black",
                },
              }}
            >
              {activeStep === steps.length - 1 ? "Finish" : "Next"}
            </Button>
          </Box>
        </Fragment>
      )}
    </Container>
  );
}
