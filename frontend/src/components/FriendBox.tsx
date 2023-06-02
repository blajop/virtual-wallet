import Avatar from "@mui/material/Avatar/Avatar";
import AvatarGroup from "@mui/material/AvatarGroup/AvatarGroup";
import Paper from "@mui/material/Paper/Paper";
import axios from "axios";
import { useEffect, useState } from "react";
import { apiUrl, baseUrl } from "../shared";
import Tooltip from "@mui/material/Tooltip/Tooltip";
import AddIcon from "@mui/icons-material/Add";

export type Friends = Friend[];

export interface Friend {
  username: string;
  email: string;
  phone: string;
  f_name: string;
  l_name: string;
  id: string;
  password: string;
  user_settings: string;
}

export default function FriendBox({ email }: { email: string }) {
  const [friends, setFriends] = useState<Friends>();
  const token: string = localStorage.token;

  useEffect(() => {
    if (email) {
      const url = apiUrl + `users/${email}/friends`; // change username
      axios
        .get(url, { headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          setFriends(response.data);
        })
        .catch((err) => console.log(err));
    }
  }, [email]);

  return (
    <>
      <Paper
        elevation={2}
        sx={{
          display: "flex",
          justifyContent: "center",
          backgroundColor: "white",
          height: "100% !important",
          width: "auto",
          padding: "20px",
          flex: "0 !important",
        }}
      >
        <AvatarGroup max={6}>
          <Tooltip title="Add friend">
            <Avatar
              sx={{ cursor: "pointer" }}
              onClick={() =>
                console.log("Not implemented. Modal popup for add friend")
              }
            >
              <AddIcon />
            </Avatar>
          </Tooltip>
          {friends?.map((friend, index) => (
            <Tooltip key={index} title={`${friend.f_name} ${friend.l_name}`}>
              <Avatar
                sx={{ cursor: "pointer" }}
                key={index}
                alt={friend?.username}
                src={`${baseUrl}static/avatars/${friend.id}.png`}
              />
            </Tooltip>
          ))}
        </AvatarGroup>
      </Paper>
    </>
  );
}
