import React from "react";

function Tile({ content, backgroundColor, className }) {
  return (
    <div
      className={`w-screen h-screen ${backgroundColor} flex items-center justify-center ${className}`}
    >
      {content}
    </div>
  );
}

export default Tile;
