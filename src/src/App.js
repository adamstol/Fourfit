import React from "react";
import { Routes, Route } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "swiper/css";

import AdvicePage from "./components/AdvicePage";
import Search from "./components/Search";

function Main() {
  const navigate = useNavigate();

  const handleNavigateSearch = () => {
    navigate("/search");
  };

  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center">
      <div className="font-nexa text-8xl font-extrabold">fourfit</div>
      <div className="font-nexa text-xl font-semibold">
        make your stylist forfeit with fourfit
      </div>
      <button
        className="outline text-2xl rounded-md mt-8 py-1 px-2 hover:underline"
        onClick={handleNavigateSearch}
      >
        shop
      </button>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/search" element={<Search />} />
      <Route path="/advice" element={<AdvicePage />} />
    </Routes>
  );
}

export default App;
