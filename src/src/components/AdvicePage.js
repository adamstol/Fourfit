import React from "react";
import FileUpload from "./FileUpload";
import eyeIcon from "../media/eye.svg";
import { useNavigate } from "react-router-dom";

function AdvicePage() {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/");
  };

  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center p-4">
      <button onClick={handleNavigate} className="-mt-32 mb-16">
        <img src={eyeIcon} alt="Navigate to Advice" />
      </button>
      <div className="h-[60vh] w-[80vw] bg-white rounded-2xl shadow-lg flex items-center justify-center">
        <FileUpload />
      </div>
    </div>
  );
}

export default AdvicePage;
