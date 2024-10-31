let isMegamenuActive = false;

const desktopMegamenuShow = () => {
  const megaMenu = document.getElementById("desktop-mega-menu");
  const megaMenuOverlay = document.getElementById("desktop-mega-menu-overlay");

  if (megaMenu && megaMenuOverlay) {
    megaMenu.classList.remove("hidden");
    megaMenuOverlay.classList.remove("hidden");
    isMegamenuActive = true;
  }
};

const desktopMegamenuHidden = () => {
  const megaMenu = document.getElementById("desktop-mega-menu");
  const megaMenuOverlay = document.getElementById("desktop-mega-menu-overlay");

  if (megaMenu && megaMenuOverlay) {
    megaMenu.classList.add("hidden");
    megaMenuOverlay.classList.add("hidden");
    isMegamenuActive = false;
  }
};

// Show Active Subcategory of Category
const categories = document.querySelectorAll("#desktopMegamenuCategory > li");
const subCategories = document.querySelectorAll("#desktopMegamenuSubCategory > div");

const showActiveMegamenu = (index) => {
  subCategories.forEach(item => item.classList.add("hidden"));
  categories.forEach(item => item.classList.remove("mega-menu-link-active"));

  if (categories[index]) {
    categories[index].classList.add("mega-menu-link-active");
  }

  if (subCategories[index]) {
    subCategories[index].classList.remove("hidden");
  }
};

categories.forEach((item, index) => {
  item.addEventListener("mouseenter", () => showActiveMegamenu(index));
});

// Active First Category on Website Mount
showActiveMegamenu(0);
