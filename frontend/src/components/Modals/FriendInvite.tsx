import * as React from "react";
import Backdrop from "@mui/material/Backdrop";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import Fade from "@mui/material/Fade";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField/TextField";
import { useEffect } from "react";
import { Friend } from "../ProfilePageComponents/FriendBox";
import axios from "axios";
import { apiUrl, baseUrl } from "../../shared";
import useDebounce from "../../hooks/useDebounce";
import { Avatar, CircularProgress, Tooltip } from "@mui/material";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import SendIcon from "@mui/icons-material/Send";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  borderRadius: "6px",
  boxShadow: 24,
  p: 4,
};

export default function TransitionsModal({
  open,
  setOpen,
  email,
  token,
  handleRefreshFriends,
}: {
  open: boolean;
  setOpen: (isOpen: boolean) => void;
  email: string;
  token: string;
  handleRefreshFriends: () => void;
}) {
  const [users, setUsers] = React.useState<Friend[]>();
  const handleClose = () => setOpen(false);

  const [searchQuery, setSearchQuery] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const debouncedSearch = useDebounce(searchQuery, 1000);

  useEffect(() => {
    if (debouncedSearch) {
      const url = apiUrl + `users?identifier=${debouncedSearch}`;
      axios
        .get(url, { headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          setUsers(response.data);
        })
        .catch((err) => console.log(err))
        .finally(() => setLoading(false));
    } else {
      setUsers([]);
      setLoading(false);
    }
  }, [debouncedSearch]);

  // function retrieveFriends(): Promise<Friend[]> {
  //   return axios
  //     .get(apiUrl + `users/${email}/friends`, {
  //       headers: { Authorization: `Bearer ${token}` },
  //     })
  //     .then((response) => response.data);
  // }

  // const [, setIsFriend] = React.useState(false);

  // const checkFriendIn = (friendUsername: string) => {
  //   retrieveFriends().then((friends) => {
  //     const isFriend = friends.some(
  //       (friend) => friend.username === friendUsername
  //     );
  //     setIsFriend(isFriend);
  //   });
  // };

  const handleAddFriend = (friend: string) => {
    const friendUrl = apiUrl + `users/${email}/friends?id=${friend}`;
    axios
      .post(friendUrl, null, { headers: { Authorization: `Bearer ${token}` } })
      .then(() => {
        handleRefreshFriends();
      })
      .catch((err) => console.log(err));
  };

  return (
    <div>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        open={open}
        onClose={handleClose}
        closeAfterTransition
        slots={{ backdrop: Backdrop }}
        slotProps={{
          backdrop: {
            timeout: 500,
          },
        }}
      >
        <Fade in={open}>
          <Box sx={style}>
            <TextField
              label="Search user"
              sx={{ width: "100%", mb: "20px" }}
              onChange={(e) => {
                setLoading(true);
                setSearchQuery(e.target.value);
              }}
            ></TextField>
            {/* Result box */}
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                gap: "5px",
                width: "100%",
                height: "250px",
              }}
            >
              {!loading ? (
                users?.slice(0, 5).map((user, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      width: "100%",
                      borderBottom: "solid gray 0.5px",
                      justifyContent: "space-between",
                      paddingBottom: "5px",
                      marginTop: "5px",
                    }}
                  >
                    <Box
                      sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: "15px",
                        borderRadius: "15px",
                      }}
                    >
                      <Avatar
                        sx={{ height: "25px", width: "25px" }}
                        alt={user?.username}
                        src={`${baseUrl}static/avatars/${user.id}.png`}
                      />
                      <Typography>
                        <strong>
                          {user.f_name} {user.l_name}
                        </strong>
                      </Typography>
                    </Box>
                    <Box sx={{ display: "flex", gap: "5px" }}>
                      <Tooltip title="Add friend">
                        <PersonAddIcon
                          fontSize="small"
                          sx={{ cursor: "pointer" }}
                          onClick={() => handleAddFriend(user.username)}
                        />
                      </Tooltip>

                      <Tooltip title="Send money">
                        <SendIcon
                          fontSize="small"
                          sx={{ cursor: "pointer" }}
                        ></SendIcon>
                      </Tooltip>
                    </Box>
                  </Box>
                ))
              ) : (
                <Box
                  sx={{
                    height: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  <CircularProgress />
                </Box>
              )}
            </Box>
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}
