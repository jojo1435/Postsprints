document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll("[counton]");

    counters.forEach(counter => {
        const inputName = counter.getAttribute("counton");
        const input = document.querySelector(`[name="${inputName}"]`);

        if (!input) return;

        const updateCounter = () => {
            const length = input.value.length;
            const max = input.getAttribute("maxlength") || "∞";

            counter.textContent = `${length} / ${max}`;

            if (input.hasAttribute("maxlength") && length >= max) {
                counter.classList.add("text-error");
            } else {
                counter.classList.remove("text-error");
            }
        };

        input.addEventListener("input", updateCounter); // escribir, borrar, pegar
        input.addEventListener("change", updateCounter);

        updateCounter();
    });
});