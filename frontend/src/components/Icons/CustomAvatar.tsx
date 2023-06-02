import { useEffect, useRef, useState } from "react";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import { baseUrl } from "../../shared";
import axios from "axios";

const CustomAvatar = () => {
  const [isHovered, setIsHovered] = useState(false);

  const [selectedImage, setSelectedImage] = useState(null);

  const fileInputRef = useRef();

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
  };

  useEffect(() => {
    if (selectedImage != null) {
      uploadImage();
    }
  }, [selectedImage]);

  const uploadImage = () => {
    const formData = new FormData();
    formData.append("file", selectedImage);
    axios
      .post(`${baseUrl}api/v1/users/profile/avatar`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("Image uploaded successfully:", response);
      })
      .catch((error) => {
        console.error("Error uploading image:", error);
      });
    localStorage.setItem(
      "avatar",
      `${localStorage.avatar}?update=${Date.now()}`
    );
    // MAY BE CHANGED
    window.location.reload();
  };

  return (
    <Box
      onClick={() => fileInputRef.current.click()}
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
          ref={fileInputRef}
          type="file"
          onChange={handleImageUpload}
          style={{ display: "none" }}
        />
      </div>
      <Avatar
        src={localStorage.getItem("avatar") ?? ""}
        sx={{
          height: "80px",
          width: "80px",
          filter: isHovered ? "brightness(80%)" : "none",
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
          <FileUploadIcon fontSize="large" />
        </Box>
      )}
    </Box>
  );
};

export default CustomAvatar;
