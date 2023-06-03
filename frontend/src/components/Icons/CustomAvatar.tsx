import { useEffect, useRef, useState } from "react";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import { baseUrl } from "../../shared";
import axios from "axios";
import React from "react";
import { AvatarContext } from "../../App";
import Tooltip from "@mui/material/Tooltip/Tooltip";

const CustomAvatar = () => {
  const { setUpdatedAvatar } = React.useContext(AvatarContext);

  const [isHovered, setIsHovered] = useState(false);

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [updatedAvatarState, setUpdatedAvatarState] = useState<string>();

  const fileInputRef = useRef<HTMLInputElement>();

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files![0];
    setSelectedImage(file);
  };

  useEffect(() => {
    setUpdatedAvatarState(`${localStorage.avatar}`);

    if (selectedImage != null) {
      uploadImage();
    }
  }, [selectedImage]);

  async function uploadImage() {
    const formData = new FormData();
    formData.append("file", selectedImage!);
    await axios
      .post(`${baseUrl}api/v1/users/profile/avatar`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        if (response.status === 200) {
        }
      })
      .catch();

    localStorage.setItem(
      "avatar",
      `${localStorage.avatar.split("?")[0]}?update=${Date.now()}`
    );
    setUpdatedAvatar(`${localStorage.avatar}`);
    setUpdatedAvatarState(`${localStorage.avatar}`);
  }

  return (
    <Tooltip title="Upload avatar">
      <Box
        onClick={() => fileInputRef.current!.click()}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        className="rounded-full cursor-pointer"
        sx={{
          position: "relative",
          display: "inline-block",
        }}
      >
        <div>
          <input
            ref={fileInputRef as React.RefObject<HTMLInputElement>}
            type="file"
            onChange={handleImageUpload}
            style={{ display: "none" }}
          />
        </div>
        <Avatar
          src={updatedAvatarState}
          sx={{
            height: "80px",
            width: "80px",
            filter: isHovered ? "brightness(40%)" : "none",
          }}
        />
        {isHovered && (
          <Box
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              zIndex: 1,
            }}
          >
            <FileUploadIcon fontSize="large" sx={{ color: "white" }} />
          </Box>
        )}
      </Box>
    </Tooltip>
  );
};

export default CustomAvatar;
