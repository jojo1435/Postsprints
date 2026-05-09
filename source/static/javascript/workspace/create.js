const icons = document.querySelectorAll("#icons-container > div");
const iconRadios = document.querySelectorAll("input[name='icon']");
const colorRadios = document.querySelectorAll("input[name='color']");

function getSelectedColor() {
    const selected = document.querySelector("input[name='color']:checked");
    return selected ? selected.value : "base";
}

function updateIconStyles() {
    const selectedColor = getSelectedColor();

    icons.forEach(icon => {
        const radio = document.querySelector(`input[name="icon"][value="${icon.id}"]`);

        icon.classList.remove(
            "border-2",
        );

        icon.className = icon.className.replace(/text-\w+-\d+/g, '');
        icon.className = icon.className.replace(/border-\w+-\d+/g, '');

        if (radio.checked) {
            icon.classList.add(
                `text-${selectedColor}-500`,
                `border-${selectedColor}-500`,
                "border-2"
            );
        } else {
            icon.classList.add("border-base-300");
        }
    });
}

icons.forEach(icon => {
    icon.addEventListener("click", () => {
        const radio = document.querySelector(`input[name="icon"][value="${icon.id}"]`);
        radio.checked = true;
        updateIconStyles();
    });
});

colorRadios.forEach(radio => {
    radio.addEventListener("change", updateIconStyles);
});

iconRadios.forEach(radio => {
    radio.addEventListener("change", updateIconStyles);
});

updateIconStyles();