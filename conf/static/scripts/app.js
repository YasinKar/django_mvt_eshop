// Scroll to Top Button
const scrollToTopButton = document.getElementById("scrollToTopButton");
if (scrollToTopButton)
  scrollToTopButton.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });

// Border Animation
const setMousePosition = (e) => {
  document.querySelectorAll(".border-gradient").forEach((item) => {
    const { left, top } = item.getBoundingClientRect();
    const { clientX, clientY } = e;
    item.style.setProperty("--x", `${clientX - left}px`);
    item.style.setProperty("--y", `${clientY - top}px`);
  });
};
document.addEventListener("mousemove", setMousePosition);


// Special Countdown
function updateCountdown() {
  const timers = document.querySelectorAll(".product-special-timer");
  const now = new Date().getTime();

  timers.forEach((timer) => {
    const expiryDate = new Date(timer.dataset.expireDate).getTime();
    const distance = expiryDate - now;
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const formattedHours = String(hours).padStart(2, "0");
    const formattedMinutes = String(minutes).padStart(2, "0");

    timer.textContent = `${days} : ${formattedHours} : ${formattedMinutes}`;

    if (distance <= 0) {
      timer.remove();
    }
  });
}

updateCountdown();
setInterval(updateCountdown, 1000);


// Progress Bar
function updateProgressBar() {
  const progressBars = document.querySelectorAll(".progress-bar");
  const now = new Date().getTime();

  progressBars.forEach((progressBar) => {
    const startDate = new Date(progressBar.dataset.startDate).getTime();
    const expiryDate = new Date(progressBar.dataset.expireDate).getTime();
    const totalDuration = expiryDate - startDate;
    const passedTime = now - startDate;
    let progress = (passedTime / totalDuration) * 100;

    progress = Math.min(Math.max(progress, 0), 100);
    progressBar.style.width = `${progress}%`;
  });
}

updateProgressBar();
setInterval(updateProgressBar, 1000);


// Countdown Wrapper
const countdownWrappers = document.querySelectorAll(".countdown-wrapper");
countdownWrappers.forEach((countdownWrapper) => {
  const expireDate = new Date(countdownWrapper.getAttribute("data-expire-date"));

  function updateBigCountdown() {
    const currentDate = new Date();
    const difference = expireDate - currentDate;

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    const secondsElement = countdownWrapper.querySelector("[data-id='seconds']");
    if (secondsElement) secondsElement.textContent = seconds;

    const minutesElement = countdownWrapper.querySelector("[data-id='minutes']");
    if (minutesElement) minutesElement.textContent = minutes;

    const hoursElement = countdownWrapper.querySelector("[data-id='hours']");
    if (hoursElement) hoursElement.textContent = hours;

    const daysElement = countdownWrapper.querySelector("[data-id='days']");
    if (daysElement) daysElement.textContent = days;
  }

  updateBigCountdown();
  setInterval(updateBigCountdown, 1000);
});


// Accordion
const accordionItems = document.querySelectorAll("[data-accordion-item]");
accordionItems.forEach((item) => {
  const button = item.querySelector("[data-accordion-button]");
  const content = item.querySelector("[data-accordion-content]");
  const chevron = item.querySelector("[data-accordion-chevron]");

  button.addEventListener("click", () => {
    const isOpen = item.classList.contains("open");
    if (isOpen) {
      item.classList.remove("open");
      content.style.maxHeight = null;
      chevron.classList.remove("-rotate-90");
    } else {
      item.classList.add("open");
      content.style.maxHeight = content.scrollHeight + "px";
      chevron.classList.add("-rotate-90");
    }
  });

  content.addEventListener("transitionend", () => {
    if (!item.classList.contains("open")) {
      content.style.maxHeight = null;
    }
  });
});


// Shop noUiSlider Initialization
const shopPriceSliders = document.querySelectorAll("[data-id='shop-price-slider']");
const shopPriceSliderMin = document.querySelectorAll("[data-id='shop-price-slider-min']");
const shopPriceSliderMax = document.querySelectorAll("[data-id='shop-price-slider-max']");

const maxPriceInput = document.querySelectorAll("#max-price-input");
const minPriceInput = document.querySelectorAll("#min-price-input");

shopPriceSliders.forEach((item) => {
  noUiSlider.create(item, {
    cssPrefix: "range-slider-",
    start: [0, 100_000_000],
    direction: "rtl",
    margin: 1,
    connect: true,
    range: {
      min: 0,
      max: 100_000_000
    },
    format: {
      to: value => value.toLocaleString("en-US", {
        style: "decimal",
        maximumFractionDigits: 0
      }),
      from: value => parseFloat(value.replace(/,/g, ""))
    }
  });

  item.noUiSlider.on("update", (values, handle) => {
    if (handle) {
      shopPriceSliderMax.forEach((priceItem) => {
        priceItem.innerHTML = values[handle];
      });
      maxPriceInput.forEach(price => {
        price.value = values[handle].replace(/,/g, "");
      })
    } else {
      shopPriceSliderMin.forEach((priceItem) => {
        priceItem.innerHTML = values[handle];
      });
      minPriceInput.forEach(price => {
        price.value = values[handle].replace(/,/g, "");
      })
    }
  });
});


// Search Filter
const searchInputWrappers = document.querySelectorAll("[data-search-item-input-wrapper]");
searchInputWrappers.forEach((wrapper) => {
  const searchInput = wrapper.querySelector("input");
  const searchItems = wrapper.nextElementSibling;

  searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value.trim().toLowerCase();
    const listItems = searchItems.querySelectorAll("li");

    listItems.forEach((item) => {
      const searchableTexts = item.querySelectorAll("[data-searchable]");
      let found = false;

      searchableTexts.forEach((textElement) => {
        const text = textElement.textContent.trim().toLowerCase();
        if (text.includes(searchTerm)) found = true;
      });

      item.style.display = found ? "block" : "none";
    });
  });
});


// Copy to Clipboard
const buttons = document.querySelectorAll("[data-copy-clipboard]");
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const textToCopy = button.getAttribute("data-copy-clipboard");
    copyToClipboard(textToCopy, button);
  });
});

function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const copyIcon = button.querySelector(".i-lucide-copy");
    const checkIcon = button.querySelector(".i-lucide-check");

    copyIcon.classList.add("hidden");
    checkIcon.classList.remove("hidden");

    setTimeout(() => {
      checkIcon.classList.add("hidden");
      copyIcon.classList.remove("hidden");
    }, 2000);
  }).catch(err => {
    console.error("Failed to copy: ", err);
  });
}


// Scroll to Element
document.querySelectorAll("[data-scroll-to]").forEach((item) => {
  item.addEventListener("click", (event) => {
    const targetId = event.currentTarget.getAttribute("data-scroll-to");
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: "smooth" });
    }
  });
});


// Show More Content

const showMoreContainers = document.querySelectorAll("[data-show-more]");
showMoreContainers.forEach((container) => {
  const content = container.querySelector("[data-show-max]");
  const button = container.querySelector("[data-show-more-button]");
  const maxHeight = parseInt(content.getAttribute("data-show-max"), 10);
  const mediaElements = container.querySelectorAll("img, video");
  let mediaLoadedCount = 0;

  const checkAndSetMaxHeight = () => {
    if (++mediaLoadedCount === mediaElements.length) {
      content.style.maxHeight = maxHeight + "px";
      if (content.scrollHeight > maxHeight) {
        button.classList.remove("hidden");
      }
    }
  };

  if (mediaElements.length === 0) {
    content.style.maxHeight = maxHeight + "px";
    if (content.scrollHeight > maxHeight) {
      button.classList.remove("hidden");
    }
  } else {
    mediaElements.forEach((media) => {
      if (media.complete) {
        checkAndSetMaxHeight();
      } else {
        media.addEventListener("load", checkAndSetMaxHeight);
        media.addEventListener("error", checkAndSetMaxHeight);
      }
    });
  }
});


// Lazy Load Stories
let lazyVideos = [...document.querySelectorAll("video.lazy-story")];

if ("IntersectionObserver" in window) {
  let lazyVideoObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      let video = entry.target;
      if (entry.isIntersecting) {
        for (let source of video.children) {
          if (typeof source.tagName === "string" && source.tagName === "SOURCE") {
            source.src = source.dataset.src;
          }
        }
        video.load();
        video.addEventListener("loadedmetadata", () => {
          video.play();
          updatePlayedTime(video);
          initializeSlider(video);
        }, { once: true });
      } else {
        video.pause();
        let barContainer = video.closest("div[data-story]").querySelector("[data-bar]");
        if (barContainer && barContainer.noUiSlider) {
          barContainer.noUiSlider.destroy();
        }
        let timeDisplay = video.closest("div[data-story]").querySelector("[data-time]");
        if (timeDisplay) {
          timeDisplay.textContent = "";
          video.removeEventListener("timeupdate", throttle(() => {
            let minutes = Math.floor(video.currentTime / 60).toString().padStart(2, "0");
            let seconds = Math.floor(video.currentTime % 60).toString().padStart(2, "0");
            timeDisplay.textContent = `${minutes}:${seconds}`;
          }, 1000));
        }
      }
    });
  });

  lazyVideos.forEach((lazyVideo) => {
    lazyVideoObserver.observe(lazyVideo);
  });
}

function updatePlayedTime(video) {
  let timeDisplay = video.closest("div[data-story]").querySelector("[data-time]");
  video.addEventListener("timeupdate", throttle(() => {
    let minutes = Math.floor(video.currentTime / 60).toString().padStart(2, "0");
    let seconds = Math.floor(video.currentTime % 60).toString().padStart(2, "0");
    timeDisplay.textContent = `${minutes}:${seconds}`;
  }, 1000));
}

function initializeSlider(video) {
  let barContainer = video.closest("div[data-story]").querySelector("[data-bar]");
  noUiSlider.create(barContainer, {
    cssPrefix: "range-slider-",
    start: 0,
    connect: "lower",
    range: {
      min: 0,
      max: video.duration
    }
  });

  barContainer.noUiSlider.on("update", throttle((values, handle) => {
    if (!video.seeking) {
      video.currentTime = values[handle];
    }
  }, 2000));

  video.addEventListener("timeupdate", throttle(() => {
    if (!video.seeking && barContainer.noUiSlider) {
      barContainer.noUiSlider.set(video.currentTime);
    }
  }, 2000));

  barContainer.noUiSlider.on("start", () => {
    video.seeking = true;
    video.pause();
  });

  barContainer.noUiSlider.on("end", (values, handle) => {
    video.seeking = false;
    video.currentTime = values[handle];
    video.play();
  });
}

lazyVideos.forEach((video) => {
  video.addEventListener("click", () => {
    let muteIcon = video.closest("div[data-story]").querySelector("[data-toggle-mute] div");
    if (video.muted) {
      video.muted = false;
      muteIcon.style.display = "none";
    } else {
      video.muted = true;
      muteIcon.style.display = "block";
    }
  });
});

function throttle(fn, wait) {
  let time = Date.now();
  return function () {
    if ((time + wait - Date.now()) < 0) {
      fn();
      time = Date.now();
    }
  };
}