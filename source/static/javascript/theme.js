const html = document.documentElement;
const toggleBtn = document.getElementById("theme-toggle");
const iconLight = document.getElementById("icon-light");
const iconDark = document.getElementById("icon-dark");

const THEMES = { light: "light", dark: "dark" };

function applyTheme(theme) {
    html.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);

    if (theme === THEMES.dark) {
        iconLight.classList.remove("hidden");
        iconDark.classList.add("hidden");
    } else {
        iconLight.classList.add("hidden");
        iconDark.classList.remove("hidden");
    }
}

function getInitialTheme() {
    const saved = localStorage.getItem("theme");
    if (saved) return saved;
    return window.matchMedia("(prefers-color-scheme: dark)").matches 
        ? THEMES.dark 
        : THEMES.light;
}

applyTheme(getInitialTheme());

toggleBtn?.addEventListener("click", () => {
    const current = html.getAttribute("data-theme");
    applyTheme(current === THEMES.dark ? THEMES.light : THEMES.dark);
});