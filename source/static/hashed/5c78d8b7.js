const mobileMenuButtons = document.querySelectorAll("[data-dashboard='button']");
const mobileMenu = document.getElementById("mobile-menu");

mobileMenuButtons.forEach(button => {
    button.addEventListener("click", function () {
        mobileMenu.classList.toggle("-translate-x-full");
    });
});