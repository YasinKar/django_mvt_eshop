// Desktop Navbar Indicator Section
const desktopNavbarIndicator = document.getElementById("desktopNavbarIndicator");
const desktopNavItems = document.querySelectorAll(".desktop-nav-item");

if (desktopNavItems) {
  desktopNavItems.forEach(item => {
    item.addEventListener("mouseenter", (e) => {
      const offsetLeft = e.currentTarget.offsetLeft;
      const offsetWidth = e.currentTarget.offsetWidth;

      desktopNavbarIndicator.style.transform = `translate3d(${offsetLeft}px, 0, 0)`;
      desktopNavbarIndicator.style.width = `${offsetWidth}px`;

      const color = e.currentTarget.dataset.color;
      if (color) {
        desktopNavbarIndicator.style.backgroundColor = color;
      }
    });

    item.addEventListener("mouseleave", () => {
      desktopNavbarIndicator.style.width = 0;
      desktopNavbarIndicator.style.backgroundColor = ""; // Reset background color
    });
  });

  // Initialize the indicator position
  const firstNavItem = desktopNavItems[0];
  if (firstNavItem) {
    const offsetLeft = firstNavItem.offsetLeft;
    desktopNavbarIndicator.style.transform = `translate3d(${offsetLeft}px, 0, 0)`;
  }
}
