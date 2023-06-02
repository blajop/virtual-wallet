import Box from "@mui/material/Box";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import Stepper from "@mui/material/Stepper";
import Typography from "@mui/material/Typography";
import { ReactNode, useState } from "react";
import axios from "axios";
import Container from "@mui/system/Container/Container";
import useValidateUsername from "../hooks/useValidateUsername.tsx";
import { apiUrl, baseUrl } from "../shared.ts";
import ButtonBlack from "../components/Buttons/ButtonBlack.tsx";
import useValidateEmail from "../hooks/useValidateEmail.tsx";
import useValidatePhone from "../hooks/useValidatePhone.tsx";
import useValidatePwd from "../hooks/useValidatePwd.tsx";
import useValidateCanSubmit from "../hooks/useValidateCanSubmit.tsx";
import useDebounce from "../hooks/useDebounce.tsx";
import RegisterForm from "../components/RegisterPageComponents/RegisterForm.tsx";
import RegisterFinish from "../components/RegisterPageComponents/RegisterFinish.tsx";
import RegisterWallet from "../components/RegisterPageComponents/RegisterWallet.tsx";

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

  const { formReg, alertConfirmPass, confirmPass, renderReg } = RegisterForm({
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

  const [token, setToken] = useState("");
  const [walletName, setWalletName] = useState("");
  const [walletCurr, setWalletCurr] = useState("BGN");

  const handleSetToken = (data: string) => {
    setToken(data);
  };
  const handleSetWalletName = (name: string) => {
    setWalletName(name);
  };
  const handleSetWalletCurr = (curr: string) => {
    setWalletCurr(curr);
  };

  const pages = [
    renderReg,
    <RegisterWallet
      username={username}
      password={password}
      setToken={handleSetToken}
      setWalletName={handleSetWalletName}
      setWalletCurr={handleSetWalletCurr}
    />,
    <RegisterFinish />,
  ];
  const [activeStep, setActiveStep] = useState(0);

  // CUSTOM HOOK USERNAME
  const debouncedUsername = useDebounce(username, 1000);

  useValidateUsername(
    debouncedUsername,
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
  const debouncedEmail = useDebounce(email, 1000);

  useValidateEmail(
    debouncedEmail,
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
  const debouncedPhone = useDebounce(phone, 1000);

  useValidatePhone(
    debouncedPhone,
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
            }
          })
          .catch();
      }
    } else if (activeStep === 1) {
      axios
        .post(
          `${apiUrl}users/${username}/wallets`,
          { currency: walletCurr, name: walletName },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => console.log("wallet created"))
        .catch((err) => console.log(err));

      setActiveStep((prevActiveStep) => prevActiveStep + 1);
    } else {
      setActiveStep((prevActiveStep) => prevActiveStep + 1);
    }
  };

  return (
    <>
      <Container
        maxWidth={"md"}
        className="pt-[100px]"
        sx={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          alignItems: "center",
        }}
      >
        <Box sx={{ width: "100%" }}>
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
                        color: "black !important",
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
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            flexDirection: "column",
            width: "100%",
          }}
        >
          {pages[activeStep]}

          <ButtonBlack
            sx={{ width: "70%", mt: "40px" }}
            onClick={handleNext}
            size="large"
            disabled={!canSubmit && activeStep != 1}
            variant="outlined"
            disabledText="Please fill in the form"
            text={activeStep === steps.length - 1 ? "Finish" : "Next step"}
          ></ButtonBlack>
        </Box>
      </Container>
    </>
  );
}
