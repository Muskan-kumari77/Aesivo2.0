import React, { useRef, useEffect } from "react";

const TryOnCanvas = ({ userImage }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const userImg = new Image();
    const clothImg = new Image();

    userImg.src = userImage;
    clothImg.src = "http://localhost:5000/static/clothes/tshirt.png";

    userImg.onload = () => {
      canvas.width = userImg.width;
      canvas.height = userImg.height;

      ctx.drawImage(userImg, 0, 0);

      // Basic overlay (centered)
      ctx.drawImage(
        clothImg,
        canvas.width * 0.25,
        canvas.height * 0.2,
        canvas.width * 0.5,
        canvas.height * 0.5
      );
    };
  }, [userImage]);

  return <canvas ref={canvasRef} />;
};

export default TryOnCanvas;