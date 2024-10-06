// AdvicePage.jsx
import React, { useState } from "react";
import FileUpload from "./FileUpload";
import magnifyingIcon from "../media/magnifying.svg";
import { useNavigate } from "react-router-dom";

function AdvicePage() {
  const navigate = useNavigate();
  const [output, setOutput] = useState(""); // State to hold the server response

  const handleNavigate = () => {
    navigate("/");
  };

  return (
    <div className="bg-mainbg min-h-screen w-screen flex flex-col items-center justify-center p-4">
      <div className="absolute left-4 top-3 font-nexa text-4xl font-bold">
        fourfit
      </div>
      <button onClick={handleNavigate} className="-mt-32 mb-16">
        <img src={magnifyingIcon} alt="Navigate to Advice" />
      </button>
      <div className="h-[60vh] w-[80vw] bg-white rounded-2xl shadow-lg flex flex-col md:flex-row items-center justify-center p-6 space-y-6 md:space-y-0 md:space-x-6">
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
