import Carousel from "./Carousel";
import eyeIcon from "../media/eye.svg";
import { useNavigate } from "react-router-dom";

function Search() {
  const navigate = useNavigate();

  const handleNavigateAdvice = () => {
    navigate("/advice");
  };

  const handleNavigateHome = () => {
    navigate("/");
  };

  return (
    <div className="bg-mainbg h-screen w-screen flex flex-col items-center justify-center">
      <div
        className="absolute left-4 top-3 font-nexa text-4xl font-extrabold hover:cursor-pointer"
        onClick={handleNavigateHome}
      >
        fourfit
      </div>

      <button onClick={handleNavigateAdvice} className="-mt-32 mb-16">
        <img src={eyeIcon} alt="Navigate to Advice" />
      </button>

      <Carousel />
    </div>
  );
}

export default Search;
