import Carousel from "./Carousel";
import eyeIcon from "../media/eye.svg";
import { useNavigate } from "react-router-dom";
import logo from "../media/fourfit_logo_black.png";

function Search() {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/advice");
  };

  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center">
      {/* <img className="absolute left-4 top-2" src={logo}></img> */}
      <div className="absolute left-4 top-3 font-nexa text-4xl font-extrabold">
        fourfit
      </div>

      <button onClick={handleNavigate} className="-mt-32 mb-16">
        <img src={eyeIcon} alt="Navigate to Advice" />
      </button>

      <Carousel />
    </div>
  );
}

export default Search;
