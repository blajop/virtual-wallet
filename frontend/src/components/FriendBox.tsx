import Avatar from "@mui/material/Avatar/Avatar";
import AvatarGroup from "@mui/material/AvatarGroup/AvatarGroup";
import Paper from "@mui/material/Paper/Paper";
import axios from "axios";
import { useEffect, useState } from "react";
import { apiUrl, baseUrl } from "../shared";
import Tooltip from "@mui/material/Tooltip/Tooltip";
import AddIcon from "@mui/icons-material/Add";
import FriendInvite from "./Modals/FriendInvite";

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

export default function FriendBox({
  email,
  refreshFriends,
  handleRefreshFriends,
}: {
  email: string;
  refreshFriends: string;
  handleRefreshFriends: () => void;
}) {
  const [friends, setFriends] = useState<Friends>();
  const [open, setOpen] = useState(false);

  const token: string = localStorage.token;

  useEffect(() => {
    if (email) {
      const url = apiUrl + `users/${email}/friends`;
      axios
        .get(url, { headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          setFriends(response.data);
        })
        .catch((err) => console.log(err));
    }
  }, [email, refreshFriends]);

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
            <Avatar sx={{ cursor: "pointer" }} onClick={() => setOpen(true)}>
              <AddIcon />
            </Avatar>
          </Tooltip>
          <FriendInvite
            handleRefreshFriends={handleRefreshFriends}
            open={open}
            setOpen={setOpen}
            email={email}
            token={token}
          ></FriendInvite>
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
