import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Paper from "@mui/material/Paper/Paper";
import TabPanel from "@mui/lab/TabPanel/TabPanel";
import TabContext from "@mui/lab/TabContext/TabContext";
import TransactionHistory from "./TransactionHistory";
import TransactionPending from "./TransactionPending";
import TransactionRecurring from "./TransactionRecurring";

export default function TransactionPanel({ username }: { username: string }) {
  const [value, setValue] = React.useState("1");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    event;
    setValue(newValue);
  };

  return (
    <Paper
      elevation={2}
      sx={{
        height: "100%",
        padding: "0px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <TabContext value={value}>
        <Tabs
          value={value}
          onChange={handleChange}
          textColor="inherit"
          aria-label="secondary tabs example"
          centered
          sx={{
            "& .MuiTabs-indicator": {
              backgroundColor: "black",
            },
            "& .MuiTab-textColorInherit": {
              color: "black",
              fontWeight: 700,
            },
          }}
        >
          <Tab
            value="1"
            label="History"
            sx={{ width: "30%", color: "black" }}
          />
          <Tab
            value="2"
            label="Pending"
            color="default"
            sx={{ width: "30%", color: "black" }}
          />
          <Tab
            value="3"
            label="Recurring"
            sx={{ width: "30%", color: "black" }}
          />
        </Tabs>
        <TabPanel value="1" sx={{ height: "100%" }}>
          <TransactionHistory username={username}></TransactionHistory>
        </TabPanel>
        <TabPanel value="2" sx={{ height: "100%" }}>
          <TransactionPending username={username} />
        </TabPanel>
        <TabPanel value="3" sx={{ height: "100%" }}>
          <TransactionRecurring username={username}></TransactionRecurring>
        </TabPanel>
      </TabContext>
    </Paper>
  );
}
