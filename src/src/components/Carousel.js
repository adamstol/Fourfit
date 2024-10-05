import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Navigation } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import Tile from "./Tile";

function Carousel() {
  const slides = [
    {
      imageSrc: "https://htv9bucket.s3.us-east-2.amazonaws.com/kyle.jpg",
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
    >
      {slides.map((slide, index) => (
        <SwiperSlide key={index} className="overflow-hidden">
          <Tile imageSrc={slide.imageSrc} />
        </SwiperSlide>
      ))}
    </Swiper>
  );
}

export default Carousel;
