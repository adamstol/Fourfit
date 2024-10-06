import React, { useState } from "react";
import heartIcon from "../media/heart.svg";

function Tile({ slide }) {
  const [isLiked, setIsLiked] = useState(false);
  const userId = "670181f33b70766a42fa8384";

  const handleClick = async () => {
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);

    const endpoint = newLikedState
      ? "http://127.0.0.1:5000/like"
      : "http://127.0.0.1:5000/unlike";

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ _id: userId, item_id: slide["_id"] }),
      });

      if (!response.ok) {
        console.error("Failed to send request, reverting state");
        setIsLiked(!newLikedState);
      }
    } catch (error) {
      console.error("Error:", error);
      setIsLiked(!newLikedState);
    }
  };

  return (
    <div className="h-full bg-white p-8 flex flex-col items-center justify-between rounded-2xl shadow-lg overflow-hidden">
      <img
        src={slide["image_src"]}
        alt="Product"
        className="h-3/4 w-auto rounded-2xl object-contain"
      />

      <button onClick={handleClick} className="m-6">
        <img
          src={heartIcon}
          alt="Like"
          className={"h-8 w-auto"}
          style={{
            filter: isLiked
              ? "invert(29%) sepia(75%) saturate(6210%) hue-rotate(345deg) brightness(94%) contrast(85%)"
              : "invert(0%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(0%) contrast(0%)",
          }}
        />
      </button>
    </div>
  );
}

export default Tile;
