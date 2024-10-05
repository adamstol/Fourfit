import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import Tile from "./Tile";

function Carousel() {
  const slides = [
    {
      content: "Slide 1",
      backgroundColor: "bg-red-500",
    },
    {
      content: "Slide 2",
      backgroundColor: "bg-blue-500",
    },
    {
      content: "Slide 3",
      backgroundColor: "bg-green-500",
    },
  ];

  return (
    <Swiper
      modules={[Pagination]}
      pagination={{
        dynamicBullets: true,
      }}
      slidesPerView={1}
      centeredSlides={true}
      loop={true}
    >
      {slides.map((slide, index) => (
        <SwiperSlide key={index} style={{ zIndex: 1 }}>
          <Tile
            content={slide.content}
            backgroundColor={slide.backgroundColor}
          />
        </SwiperSlide>
      ))}
    </Swiper>
  );
}

export default Carousel;
