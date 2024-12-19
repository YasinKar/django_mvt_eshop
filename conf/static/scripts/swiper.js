// Define common breakpoints
const commonBreakpoints = {
  0: { slidesPerView: 2.1, spaceBetween: 6 },
  480: { slidesPerView: 2.8, spaceBetween: 15 },
  640: { slidesPerView: 3.3, spaceBetween: 15 },
  768: { slidesPerView: 4, spaceBetween: 15 },
  1024: { slidesPerView: 5, spaceBetween: 20 },
  1280: { slidesPerView: 6, spaceBetween: 20 }
};

// Function to initialize Swipers
function initializeSwiper(selector, config) {
  new Swiper(selector, config);
}

// Main banner swiper
initializeSwiper(".main-banner", {
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true
  },
  autoplay: {
    delay: 6000,
    disableOnInteraction: false
  },
  speed: 600
});

// Product slider
initializeSwiper(".product-slider", {
  freeMode: true,
  breakpoints: {
    ...commonBreakpoints,
    1024: { slidesPerView: 5, spaceBetween: 20 }
  }
});

// Product slider wrapped
initializeSwiper(".product-slider-wrapped", {
  slidesPerView: 1.7,
  spaceBetween: 2,
  freeMode: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  breakpoints: {
    360: { slidesPerView: 2, spaceBetween: 2 },
    460: { slidesPerView: 2.5, spaceBetween: 2 },
    640: { slidesPerView: 3.3, spaceBetween: 2 },
    768: { slidesPerView: 3.8, spaceBetween: 2 },
    1024: { slidesPerView: 5.5, spaceBetween: 2 },
    1380: { slidesPerView: 6, spaceBetween: 2 }
  }
});

// Blog swiper
initializeSwiper(".blog-swiper", {
  slidesPerView: 1.3,
  spaceBetween: 14,
  freeMode: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  breakpoints: {
    360: { slidesPerView: 1.4, spaceBetween: 10 },
    460: { slidesPerView: 1.8, spaceBetween: 15 },
    640: { slidesPerView: 2.4, spaceBetween: 10 },
    768: { slidesPerView: 2.8, spaceBetween: 15 },
    1024: { slidesPerView: 4, spaceBetween: 20 },
    1380: { slidesPerView: 4, spaceBetween: 20 }
  }
});

// Brand slider
initializeSwiper(".brand-slider", {
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  freeMode: true,
  breakpoints: commonBreakpoints
});

// Search result slider
initializeSwiper(".search-result-slider", {
  slidesPerView: 1.3,
  spaceBetween: 10,
  freeMode: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  breakpoints: {
    360: { slidesPerView: 1.5, spaceBetween: 10 },
    460: { slidesPerView: 2.2, spaceBetween: 10 },
    640: { slidesPerView: 2.5, spaceBetween: 10 },
    1024: { slidesPerView: 2.8, spaceBetween: 10 },
    1380: { slidesPerView: 3.5, spaceBetween: 10 }
  }
});

// Small product image swiper
initializeSwiper(".small-product-image-swiper", {
  slidesPerView: 3,
  spaceBetween: 10,
  freeMode: true,
  breakpoints: {
    360: { slidesPerView: 3, spaceBetween: 10 },
    460: { slidesPerView: 4, spaceBetween: 10 },
    640: { slidesPerView: 5, spaceBetween: 10 },
    768: { slidesPerView: 6, spaceBetween: 10 },
    1380: { slidesPerView: 8, spaceBetween: 10 }
  }
});

// Product gallery mobile swiper
initializeSwiper(".product-gallery-mobile-swiper", {
  pagination: {
    el: ".swiper-pagination"
  }
});

// Product gallery swiper
initializeSwiper(".product-gallery-swiper", {
  pagination: {
    el: ".swiper-pagination"
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  }
});

// Product comment swiper
initializeSwiper(".product-comment-swiper", {
  freeMode: true,
  breakpoints: {
    0: { slidesPerView: 1.1, spaceBetween: 10 },
    360: { slidesPerView: 1.2, spaceBetween: 10 },
    460: { slidesPerView: 1.6, spaceBetween: 10 },
    640: { slidesPerView: 2.2, spaceBetween: 10 }
  }
});

// Story slider
initializeSwiper(".story-slider", {
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  freeMode: true,
  breakpoints: {
    0: { slidesPerView: 3.2, spaceBetween: 6 },
    340: { slidesPerView: 3.5, spaceBetween: 6 },
    400: { slidesPerView: 4, spaceBetween: 6 },
    480: { slidesPerView: 4.5, spaceBetween: 15 },
    640: { slidesPerView: 6.5, spaceBetween: 15 },
    768: { slidesPerView: 7.5, spaceBetween: 15 },
    1024: { slidesPerView: 9.5, spaceBetween: 20 },
    1280: { slidesPerView: 12.5, spaceBetween: 20 }
  }
});

// Story product slider
initializeSwiper(".story-product-slider", {
  slidesPerView: 1.5,
  spaceBetween: 10,
  freeMode: true,
  breakpoints: {
    360: { slidesPerView: 1.3, spaceBetween: 10 }
  }
});

// Best sale hour slider
initializeSwiper(".best-sale-hour-slider", {
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  freeMode: true,
  breakpoints: {
    0: { slidesPerView: 1.1, spaceBetween: 6 },
    480: { slidesPerView: 1.6, spaceBetween: 15 },
    640: { slidesPerView: 2.2, spaceBetween: 15 },
    768: { slidesPerView: 2.6, spaceBetween: 15 },
    1024: { slidesPerView: 3.3, spaceBetween: 20 },
    1280: { slidesPerView: 4, spaceBetween: 20 }
  }
});

// Shop category slider
initializeSwiper(".shop-category-slider", {
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  freeMode: true,
  breakpoints: commonBreakpoints
});
