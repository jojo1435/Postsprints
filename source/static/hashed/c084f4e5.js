(function () {
	const STRENGTH_LEVELS = [
		{ label: "",       color: "accent",   value: 0   },
		{ label: "Weak",   color: "error",    value: 25  },
		{ label: "Fair",   color: "warning",  value: 50  },
		{ label: "Good",   color: "info",     value: 75  },
		{ label: "Strong", color: "success",  value: 100 },
	];

	function scorePassword(password) {
		if (!password) return 0;
		let score = 0;
		score += Math.min(password.length * 4, 40);
		if (/[a-z]/.test(password))        score += 10;
		if (/[A-Z]/.test(password))        score += 15;
		if (/\d/.test(password))           score += 15;
		if (/[^a-zA-Z0-9]/.test(password)) score += 20;
		return Math.min(score, 100);
	}

	function getStrengthLevel(score) {
		if (score === 0)  return STRENGTH_LEVELS[0];
		if (score <= 25)  return STRENGTH_LEVELS[1];
		if (score <= 50)  return STRENGTH_LEVELS[2];
		if (score <= 75)  return STRENGTH_LEVELS[3];
		return STRENGTH_LEVELS[4];
	}

	function findInput(wrapper) {
		return wrapper.querySelector('input[type="password"], input[type="text"]');
	}

	const EYE_OPEN_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
		stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
		class="h-[1em] opacity-50 pointer-events-none">
		<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
		<circle cx="12" cy="12" r="3"/>
	</svg>`;

	const EYE_CLOSED_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
		stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
		class="h-[1em] opacity-50 pointer-events-none">
		<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
		<path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
		<line x1="1" y1="1" x2="23" y2="23"/>
	</svg>`;

	function injectToggle(wrapper) {
		const input = findInput(wrapper);
		if (!input || wrapper.querySelector(".pw-toggle-btn")) return;

		const btn = document.createElement("button");
		btn.type = "button";
		btn.className = "pw-toggle-btn btn btn-ghost btn-xs px-1 ml-1 opacity-60 hover:opacity-100 transition-opacity";
		btn.setAttribute("aria-label", "Show password");
		btn.innerHTML = EYE_OPEN_SVG;

		btn.addEventListener("click", () => {
			const isPassword = input.type === "password";
			input.type = isPassword ? "text" : "password";
			btn.innerHTML = isPassword ? EYE_CLOSED_SVG : EYE_OPEN_SVG;
			btn.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
		});

		wrapper.appendChild(btn);
	}


	const PROGRESS_COLOR_CLASSES = [
		"progress-error", "progress-warning",
		"progress-info",  "progress-success", "progress-accent",
	];

	function wireStrengthMeter(wrapper) {
		const input = findInput(wrapper);
		if (!input) return;

		let sibling = wrapper.nextElementSibling;
		let progress = null;
		let label = null;

		while (sibling) {
			progress = sibling.querySelector("progress");
			if (progress) {
			label = sibling.querySelector("p:last-child");
			break;
			}
			sibling = sibling.nextElementSibling;
		}

		if (!progress || !label) return;

		function updateStrength() {
			const score = scorePassword(input.value);
			const level = getStrengthLevel(score);

			progress.value = level.value;
			PROGRESS_COLOR_CLASSES.forEach((c) => progress.classList.remove(c));
			if (level.color) progress.classList.add(`progress-${level.color}`);
			label.textContent = level.label ? `Strength: ${level.label}` : "Strength: —";
		}

		input.addEventListener("input", updateStrength);

		if (input.value) updateStrength();
	}

	function init() {
		document.querySelectorAll("label.input").forEach((wrapper) => {
		if (!findInput(wrapper)) return;
			injectToggle(wrapper);
			wireStrengthMeter(wrapper);
		});
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", init);
	} else {
		init();
	}
})();