import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";
import Typography from "@mui/material/Typography";
import { Fragment, ReactNode, useState } from "react";
import Register from "../components/Signup";
import Home from "./Home";
import axios, { AxiosError } from "axios";
import Collapse from "@mui/material/Collapse";
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";

const steps = ["New User", "Two", "Aide"];

export default function RegisterStepper() {
  const { form, render } = Register();
  const pages = [render, <Home />];
  const [dataCheck, setDataCheck] = useState(false);
  const [alert, setAlert] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [activePage, setActivePage] = useState(0);

  // NEXT BUTTON HANDLER
  const handleNext = () => {
    if (activeStep === 0) {
      axios
        .post("http://localhost:8000/api/v1/data-unique", form)
        .then((response) => {
          console.log(response.data);
          if (response.status === 200) {
            setDataCheck(true);
            console.log(form);
          }
        })
        .catch((err: AxiosError) => {
          console.log(err.response.data);
          setAlert(true);
        });
    }

    // setActiveStep((prevActiveStep) => prevActiveStep + 1);
    // setActivePage((prevActivePage) => prevActivePage + 1);
  };
  // BACK BUTTON HANDLER
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
    setActivePage((prevActivePage) => prevActivePage - 1);
  };

  return (
    <Box sx={{ width: "100%" }}>
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
          <Typography sx={{ mt: 2, mb: 1 }}>{pages[activePage]}</Typography>
          <Box sx={{ display: "flex", flexDirection: "row", pt: 2 }}>
            {/* BACK BUTTON */}
            <Button
              color="inherit"
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>

            {/* NEXT BUTTON */}
            <Button onClick={handleNext}>
              {activeStep === steps.length - 1 ? "Finish" : "Next"}
            </Button>
          </Box>
          <Collapse in={alert}>
            <Alert severity="error">
              <AlertTitle>
                <strong>Data Taken!</strong>
              </AlertTitle>
            </Alert>
          </Collapse>
        </Fragment>
      )}
    </Box>
  );
}
