import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";
import Typography from "@mui/material/Typography";
import { Fragment, ReactNode, useState, useEffect } from "react";
import SignupForm from "../components/SignupForm.tsx";
import axios, { AxiosError } from "axios";
import Container from "@mui/system/Container/Container";
// import { baseUrl } from "../shared.js";
import useValidateUsername from "../hooks/useValidateUsername.tsx";
import { baseUrl } from "../shared.ts";
import ButtonBlack from "../components/Buttons/ButtonBlack.tsx";
import debounce from "@mui/material/utils/debounce";
import { createTheme, ThemeProvider } from "@mui/material/styles";

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

// const USERNAME_REGEX = /^.{2,20}$/;
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const PHONE_REGEX = /^\d{10}$/;
const PWD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$/;
// const PWD_INSTRUCTION = "...";
// const SIGNUP_URL = baseUrl + "api/v1/signup";

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

  // CUSTOM HOOK
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

  const [canSubmit, setCanSubmit] = useState(false);

  const pages = [renderReg];
  const [activeStep, setActiveStep] = useState(0);
  const [activePage, setActivePage] = useState(0);

  // USERNAME VALIDATIONS
  // useEffect(() => {
  //   if (username != "") {
  //     if (!USERNAME_REGEX.test(username)) {
  //       setAlertUsername(true);
  //       setAlertMsgUsername("Username should be [2,20] chars long");
  //     } else {
  //       setAlertUsername(false);
  //       setAlertMsgUsername("");

  //       setTimeout(() => {
  //         axios
  //           .get(`http://localhost:8000/api/v1/username-unique/${username}`)
  //           .then((response) => {
  //             console.log(response.data);
  //             if (response.status === 200) {
  //               setAlertUsername(false);
  //               setAlertMsgUsername("");
  //             }
  //           })
  //           .catch(() => {
  //             setAlertUsername(true);
  //             setAlertMsgUsername("Username is already taken");
  //           });
  //       }, 500);
  //     }
  //   } else {
  //     setAlertUsername(false);
  //     setAlertMsgUsername("");
  //   }
  // }, [username]);

  // EMAIL VALIDATIONS
  useEffect(() => {
    if (email != "") {
      if (!EMAIL_REGEX.test(email)) {
        setAlertEmail(true);
        setAlertMsgEmail("You should enter email input");
      } else {
        setAlertEmail(false);
        setAlertMsgEmail("");

        setTimeout(() => {
          axios
            .get(`${baseUrl}api/v1/email-unique/${email}`)
            .then((response) => {
              console.log(response.data);
              if (response.status === 200) {
                setAlertEmail(false);
                setAlertMsgEmail("");
              }
            })
            .catch(() => {
              setAlertEmail(true);
              setAlertMsgEmail("Email is already taken");
            });
        }, 500);
      }
    } else {
      setAlertEmail(false);
      setAlertMsgEmail("");
    }
  }, [email]);

  // PHONE VALIDATIONS
  useEffect(() => {
    setAlertPhone(false);
    setAlertMsgPhone("");
    const checkPhoneAvailability = debounce(() => {
      axios
        .get(`${baseUrl}api/v1/phone-unique/${phone}`)
        .then((response) => {
          if (response.status === 200) {
            setAlertPhone(false);
            setAlertMsgPhone("");
          }
        })
        .catch(() => {
          setAlertPhone(true);
          setAlertMsgPhone("Phone number is already taken");
        });
    }, 1500);

    if (phone !== "") {
      if (!PHONE_REGEX.test(phone)) {
        setAlertPhone(true);
        setAlertMsgPhone("Phone should be a valid 10-digit number");
        return;
      }
      checkPhoneAvailability();
    } else {
      setAlertPhone(false);
      setAlertMsgPhone("");
    }
  }, [phone]);

  // PASSWORD VALIDATION
  useEffect(() => {
    if (password != "") {
      if (!PWD_REGEX.test(password)) {
        setAlertPwd(true);
        setAlertMsgPwd(
          "Password must be at least 8 characters - at least one uppercase, lowercase, digit, symbol"
        );
      } else {
        setAlertPwd(false);
        setAlertMsgPwd("");
      }
    } else {
      setAlertPwd(false);
      setAlertMsgPwd("");
    }
  }, [password]);

  // CAN_SUBMIT VALIDATION
  useEffect(() => {
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
      confirmPass,
    ];
    if (
      conditions.every((element) => element === true) &&
      conditions2.every((element) => element != "")
    ) {
      setCanSubmit(true);
    } else {
      setCanSubmit(false);
    }
  });

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
          {steps.map((label, index) => {
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
