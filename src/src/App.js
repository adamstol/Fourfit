import React from "react";
import { Routes, Route } from "react-router-dom";
import "swiper/css";

import AdvicePage from "./components/AdvicePage";
import Search from "./components/Search";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Search />} />
      <Route path="/advice" element={<AdvicePage />} />
    </Routes>
  );
}

export default App;
