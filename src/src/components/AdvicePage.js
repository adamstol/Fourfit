// AdvicePage.jsx
import React, { useState } from "react";
import FileUpload from "./FileUpload";
import magnifyingIcon from "../media/magnifying.svg";
import { useNavigate } from "react-router-dom";

function AdvicePage() {
  const navigate = useNavigate();
  const [output, setOutput] = useState(""); // State to hold the server response

  const handleNavigateSearch = () => {
    navigate("/search");
  };

  const handleNavigateHome = () => {
    navigate("/");
  };

  return (
    <div className="bg-mainbg min-h-screen w-screen flex flex-col items-center justify-center p-4">
      <div
        onClick={handleNavigateHome}
        className="absolute left-4 top-3 font-nexa text-4xl font-bold hover:cursor-pointer"
      >
        fourfit
      </div>
      <button onClick={handleNavigateSearch} className="-mt-32 mb-16">
        <img src={magnifyingIcon} alt="Navigate to Advice" />
      </button>
      <div className="h-[60vh] w-[70vw] bg-white rounded-2xl shadow-lg flex flex-col items-center justify-center p-6 space-y-6">
        <FileUpload setOutput={setOutput} />
        {output && (
          <div
            id="output"
            className="w-full md:w-1/2 p-4 overflow-auto border rounded"
            dangerouslySetInnerHTML={{ __html: output }}
          ></div>
        )}
      </div>
    </div>
  );
}

export default AdvicePage;
