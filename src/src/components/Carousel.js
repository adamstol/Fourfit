import React, { useEffect, useState, useCallback } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Navigation } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import Tile from "./Tile";

function Carousel() {
  const [slides, setSlides] = useState([]);
  const userId = "670181f33b70766a42fa8384";

  const fetchSlides = useCallback(async () => {
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
        }
      } else {
        console.error("Failed to fetch slides");
      }
    } catch (error) {
      console.error("Error fetching slides:", error);
    }
  }, [userId]);

  useEffect(() => {
    fetchSlides();
  }, [fetchSlides]);

  return (
    <Swiper
      modules={[Navigation, Pagination]}
      navigation
      pagination={{
        dynamicBullets: true,
      }}
      freeMode={true}
      slidesPerView={1}
      centeredSlides={true}
      spaceBetween={20}
      className="h-[60vh] w-[80vw] overflow-hidden rounded-2xl shadow-2xl"
      onSlideChange={(swiper) => {
        if (swiper.activeIndex >= slides.length - 2) {
          fetchSlides();
        }
      }}
    >
      {slides.map((slide, index) => (
        <SwiperSlide key={index} className="overflow-hidden">
          <Tile slide={slide} />
        </SwiperSlide>
      ))}
    </Swiper>
  );
}

export default Carousel;
