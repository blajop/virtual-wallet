import React, { useEffect, useState } from "react";
import axios from "axios";
import { baseUrl } from "../../shared";

const CustomAvatar = () => {
  const [selectedImage, setSelectedImage] = useState(null);

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
  };

  return (
    <div>
      <input type="file" onChange={handleImageUpload} />
      {/* <button onClick={uploadImage}>Upload</button> */}
    </div>
  );
};

export default CustomAvatar;
