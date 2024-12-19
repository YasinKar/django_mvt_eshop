const theme = localStorage.getItem("theme")

const isDark = () => {
  return document.documentElement.classList.contains("dark");
};
const setThemeInfo = () => {
  document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", isDark() ? "dark" : "light");
};

const isAppearanceTransition =
  typeof document !== "undefined" &&
  document.startViewTransition &&
  !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function toggleDark(event) {
  if (!isAppearanceTransition || !event) {
    setThemeInfo();
    return;
  }

  const x = event.clientX;
  const y = event.clientY;
  const endRadius = Math.hypot(
    Math.max(x, innerWidth - x),
    Math.max(y, innerHeight - y)
  );

  const transition = document.startViewTransition(async () => {
    setThemeInfo();
  });

  transition.ready.then(() => {
    const clipPath = [
      `circle(0px at ${x}px ${y}px)`,
      `circle(${endRadius}px at ${x}px ${y}px)`,
    ];
    document.documentElement.animate(
      {
        clipPath: isDark() ? [...clipPath].reverse() : clipPath,
      },
      {
        duration: 500,
        easing: "ease-in",
        pseudoElement: isDark()
          ? "::view-transition-old(root)"
          : "::view-transition-new(root)",
      }
    );
  });
}
