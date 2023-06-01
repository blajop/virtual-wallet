import Box from "@mui/material/Box";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";
import Typography from "@mui/material/Typography";
import { Fragment, ReactNode, useState } from "react";
import SignupForm from "../components/SignupForm.tsx";
import axios, { AxiosError } from "axios";
import Container from "@mui/system/Container/Container";
import useValidateUsername from "../hooks/useValidateUsername.tsx";
import { baseUrl } from "../shared.ts";
import ButtonBlack from "../components/Buttons/ButtonBlack.tsx";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import useValidateEmail from "../hooks/useValidateEmail.tsx";
import useValidatePhone from "../hooks/useValidatePhone.tsx";
import useValidatePwd from "../hooks/useValidatePwd.tsx";
import useValidateCanSubmit from "../hooks/useValidateCanSubmit.tsx";

const theme = createTheme({
  components: {
    MuiStepIcon: {
      styleOverrides: {
        root: {
          "&$completed": {
            color: "pink",
          },
          "&$active": {
            color: "red",
          },
        },
        active: {},
        completed: {},
      },
    },
  },
});

const steps = ["Register", "Create Wallet", "Final steps"];

export default function RegisterStepper() {
  const [alertUsername, setAlertUsername] = useState(false);
  const [alertMsgUsername, setAlertMsgUsername] = useState("");

  const [alertEmail, setAlertEmail] = useState(false);
  const [alertMsgEmail, setAlertMsgEmail] = useState("");

  const [alertPhone, setAlertPhone] = useState(false);
  const [alertMsgPhone, setAlertMsgPhone] = useState("");

  const [alertPwd, setAlertPwd] = useState(false);
  const [alertMsgPwd, setAlertMsgPwd] = useState("");

  const { formReg, alertConfirmPass, confirmPass, renderReg } = SignupForm({
    alertUsername: alertUsername,
    alertMsgUsername: alertMsgUsername,
    alertEmail: alertEmail,
    alertMsgEmail: alertMsgEmail,
    alertPhone: alertPhone,
    alertMsgPhone: alertMsgPhone,
    alertPwd: alertPwd,
    alertMsgPwd: alertMsgPwd,
  });

  const username = formReg["username"];
  const email = formReg["email"];
  const phone = formReg["phone"];
  const password = formReg["password"];

  const [canSubmit, setCanSubmit] = useState(false);

  const pages = [renderReg];
  const [activeStep, setActiveStep] = useState(0);
  const [activePage, setActivePage] = useState(0);

  // CUSTOM HOOK USERNAME
  useValidateUsername(
    username,
    [
      alertUsername,
      (value: boolean) => {
        setAlertUsername(value);
        return value;
      },
    ],
    [
      alertMsgUsername,
      (value: string) => {
        setAlertMsgUsername(value);
        return value;
      },
    ]
  );

  // CUSTOM HOOK EMAIL
  useValidateEmail(
    email,
    [
      alertEmail,
      (value: boolean) => {
        setAlertEmail(value);
        return value;
      },
    ],
    [
      alertMsgEmail,
      (value: string) => {
        setAlertMsgEmail(value);
        return value;
      },
    ]
  );

  // CUSTOM HOOK PHONE
  useValidatePhone(
    phone,
    [
      alertPhone,
      (value: boolean) => {
        setAlertPhone(value);
        return value;
      },
    ],
    [
      alertMsgPhone,
      (value: string) => {
        setAlertMsgPhone(value);
        return value;
      },
    ]
  );

  // CUSTOM HOOK PASSWORD
  useValidatePwd(
    password,
    [
      alertPwd,
      (value: boolean) => {
        setAlertPwd(value);
        return value;
      },
    ],
    [
      alertMsgPwd,
      (value: string) => {
        setAlertMsgPwd(value);
        return value;
      },
    ]
  );

  // CUSTOM HOOK CAN SUBMIT
  useValidateCanSubmit(
    [
      canSubmit,
      (value: boolean) => {
        setCanSubmit(value);
        return value;
      },
    ],

    alertConfirmPass,
    alertUsername,
    alertEmail,
    alertPhone,
    formReg["f_name"],
    formReg["l_name"],
    formReg["username"],
    formReg["email"],
    formReg["phone"],
    formReg["password"],
    confirmPass
  );

  // NEXT BUTTON HANDLER
  const handleNext = () => {
    if (activeStep === 0) {
      if (canSubmit === true) {
        axios
          .post(`${baseUrl}api/v1/signup`, formReg)
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
    <ThemeProvider theme={theme}>
      <Container
        maxWidth={"md"}
        className="pt-[100px]"
        sx={{ display: "flex", flexDirection: "column", height: "120%" }}
      >
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => {
            const stepProps: { completed?: boolean } = {};
            const labelProps: {
              optional?: ReactNode;
            } = {};
            return (
              <Step key={label} {...stepProps}>
                <StepLabel
                  sx={{
                    ".Mui-active": { color: "black !important" },
                    ".Mui-completed": {
                      color: "black",
                    },
                  }}
                  {...labelProps}
                >
                  <Typography>{label}</Typography>
                </StepLabel>
              </Step>
            );
          })}
        </Stepper>

        {activeStep === steps.length ? (
          <Fragment>
            <Typography sx={{ mt: 2, mb: 1 }}>You are all set!</Typography>
          </Fragment>
        ) : (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              flexDirection: "column",
              width: "100%",
            }}
          >
            {/* ACTIVE PAGE IS NESTED HERE BUTTON */}
            {pages[activePage]}

            {/* NEXT BUTTON */}
            <ButtonBlack
              sx={{ width: "70%", mt: "40px" }}
              onClick={handleNext}
              size="large"
              disabled={!canSubmit}
              variant="outlined"
              disabledText="Please fill in the form"
              text={activeStep === steps.length - 1 ? "Finish" : "Next step"}
            ></ButtonBlack>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}
