import React, { useState } from "react";
import TryOnCanvas from "./TryOnCanvas";

const TryOnPage = () => {
  const [image, setImage] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch("http://localhost:5000/api/tryon/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setImage(data.image_url);
  };

  return (
    <div>
      <h2>Virtual Try-On</h2>

      <input type="file" onChange={handleUpload} />

      {image && <TryOnCanvas userImage={image} />}
    </div>
  );
};

export default TryOnPage;