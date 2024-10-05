import React from "react";
import { useNavigate, Routes, Route } from "react-router-dom";
import "swiper/css";
import Carousel from "./components/Carousel";
import eyeIcon from "./media/eye.svg";
import AdvicePage from "./components/AdvicePage";

function Main() {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/advice");
  };

  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center">
      <button onClick={handleNavigate} className="-mt-32 mb-16">
        <img src={eyeIcon} alt="Navigate to Advice" />
      </button>

      <Carousel />
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/advice" element={<AdvicePage />} />
    </Routes>
  );
}

export default App;
