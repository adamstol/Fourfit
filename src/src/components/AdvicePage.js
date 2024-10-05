import React from "react";
import FileUpload from "./FileUpload";

function AdvicePage() {
  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center p-4">
      <div className="h-[60vh] w-[80vw] bg-white rounded-2xl shadow-lg flex items-center justify-center">
        <FileUpload />
      </div>
    </div>
  );
}

export default AdvicePage;
