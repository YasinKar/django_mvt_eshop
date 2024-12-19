const elementsWithScrollClass = document.querySelectorAll('[data-onscrollclass]');

let isScrollingDown = false;
let prevScrollPos = document.documentElement.scrollTop;

const handleScroll = () => {
    const currentScrollPos = document.documentElement.scrollTop;

    if (currentScrollPos > prevScrollPos && !isMegamenuActive && currentScrollPos > 60) {
        // Scrolling Down
        elementsWithScrollClass.forEach(element => {
            element.classList.add(element.dataset.onscrollclass);
        });
        isScrollingDown = true;
    } else {
        // Scrolling Up
        elementsWithScrollClass.forEach(element => {
            element.classList.remove(element.dataset.onscrollclass);
        });
        isScrollingDown = false;
    }

    prevScrollPos = currentScrollPos;
};

window.addEventListener("scroll", handleScroll);
