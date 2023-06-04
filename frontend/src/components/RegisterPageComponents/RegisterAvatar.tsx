import Paper from "@mui/material/Paper/Paper";
import Typography from "@mui/material/Typography/Typography";
import CustomAvatar from "../Icons/CustomAvatar";
import { useState } from "react";

function RegisterAvatar({
  token,
  onAvatarUploaded,
}: {
  token: string;
  onAvatarUploaded: () => void;
}) {
  const [uploadAvatar, setUploadAvatar] = useState<string>("");

  const onUploadAvatar = (url: string) => setUploadAvatar(url);
  return (
    <>
      <Paper
        sx={{
          width: "70%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          mt: "40px",
          padding: "40px",
        }}
      >
        <Typography variant="h3" className="mb-5">
          Almost done!
        </Typography>
        <CustomAvatar
          onAvatarUploaded={onAvatarUploaded}
          onUploadAvatar={onUploadAvatar}
          token={token}
          src={uploadAvatar}
        ></CustomAvatar>
        <Typography
          textAlign={"center"}
          sx={{ marginTop: "40px", width: "60%" }}
        >
          In order to protect your account, we would require you to upload an
          image of yourself
        </Typography>
      </Paper>
    </>
  );
}

export default RegisterAvatar;
