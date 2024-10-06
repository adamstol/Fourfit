import React, { useEffect, useState, useCallback } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Navigation } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import Tile from "./Tile";
import spinner from "../media/spinner.svg";

function Carousel() {
  const [slides, setSlides] = useState([]);
  const [isFetching, setIsFetching] = useState(true);
  const userId = "670181f33b70766a42fa8384";

  const fetchSlides = useCallback(async () => {
    setIsFetching(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ _id: userId }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          console.log(data.items);
          setSlides((prevSlides) => [...prevSlides, ...data.items]);
        } else {
          console.error("Fetch failed: success flag false");
        }
      } else {
        console.error("Failed to fetch slides: ", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching slides:", error);
    } finally {
      setIsFetching(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchSlides();
  }, [fetchSlides]);

  return (
    <div className="relative h-[60vh] w-[70vw]">
      {isFetching && slides.length === 0 && (
        <div className="flex animate-spin justify-center items-center h-full">
          <img src={spinner} alt="Loading..." className="w-12 h-12" />
        </div>
      )}

      {!isFetching || slides.length > 0 ? (
        <Swiper
          modules={[Navigation, Pagination]}
          navigation={true}
          pagination={{
            dynamicBullets: true,
          }}
          freeMode={true}
          slidesPerView={1}
          centeredSlides={true}
          spaceBetween={20}
          className="h-full w-full overflow-hidden rounded-2xl shadow-lg bg-white"
          onSlideChange={(swiper) => {
            if (swiper.activeIndex >= slides.length - 2 && !isFetching) {
              fetchSlides();
            }
          }}
        >
          {slides.map((slide, index) => (
            <SwiperSlide key={index} className="overflow-hidden">
              <Tile slide={slide} />
            </SwiperSlide>
          ))}

          {isFetching && slides.length > 0 && (
            <div className="absolute animate-spin bottom-4 left-1/2 transform -translate-x-1/2 flex items-center space-x-2">
              <img src={spinner} alt="Loading more..." className="w-8 h-8" />
              <span>Loading more...</span>
            </div>
          )}
        </Swiper>
      ) : null}
    </div>
  );
}

export default Carousel;
