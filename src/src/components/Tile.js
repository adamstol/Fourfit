import React, { useState } from "react";
import heartIcon from "../media/heart.svg";
import bagIcon from "../media/bag.svg";

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
    <div className="h-full bg-white p-8 flex flex-row items-center justify-center rounded-2xl shadow-lg overflow-hidden">
      <img
        src={slide["image_src"]}
        alt="Product"
        className="h-5/6 w-auto rounded-2xl object-contain"
      />

      <div className="my-8 px-4">
        <div className="text-3xl">
          {slide["product_link"]
            .split(".")[1]
            .replace(/\b\w/g, (char) => char.toUpperCase())}{" "}
          {slide["item_type"].replace(/\b\w/g, (char) => char.toUpperCase())}
        </div>
        <div className="text-gray-400">
          {slide["tags"].map((tag) => `#${tag}`).join(", ")}
        </div>

        <div className="flex flex-row pt-2">
          <button onClick={handleClick} className="mr-6 pt-[2px]">
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

          <a href={slide["product_link"]} target="_blank">
            <img
              src={bagIcon}
              alt="Redirect to Product Page"
              href={slide["product_link"]}
              className={"h-8 w-auto"}
              style={{
                filter:
                  "invert(0%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(0%) contrast(0%)",
              }}
            />
          </a>
        </div>
      </div>
    </div>
  );
}

export default Tile;
