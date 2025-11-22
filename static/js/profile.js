document.addEventListener("DOMContentLoaded", () => {

    animateOnLoad(".profile-card", 120);
    animateOnLoad(".profile-section", 120);

    initProfileForms();
    initThemeToggle();
    initLimitForm();
});

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}

function initProfileForms() {

    const profileForm = document.getElementById("profileForm");

    if (profileForm) {
        profileForm.addEventListener("submit", (e) => {

            e.preventDefault();

            const formData = new FormData(profileForm);

            fetch("/profile/update", {
                    method: "POST",
                    body: formData
                })
                .then(r => r.json())
                .then(data => {

                    if (data.success) {
                        showToast("Profile updated successfully!", "success");

                        // Animate updated fields (subtle glow)
                        animateUpdatedFields(profileForm);
                    } else {
                        showToast(data.message || "Failed to update profile.", "error");
                    }
                });
        });
    }
}

function animateUpdatedFields(form) {

    form.querySelectorAll("input, select").forEach(input => {
        input.classList.add("updated-flash");
        setTimeout(() => input.classList.remove("updated-flash"), 800);
    });

    // Auto-inject CSS (once)
    if (!document.getElementById("updatedFlashStyles")) {
        const style = document.createElement("style");
        style.id = "updatedFlashStyles";
        style.innerHTML = `
        .updated-flash {
            box-shadow: 0 0 12px rgba(108,99,255,0.7) !important;
            transition: box-shadow .4s ease;
        }
        `;
        document.head.appendChild(style);
    }
}

function initThemeToggle() {

    const toggle = document.getElementById("themeToggle");
    if (!toggle) return;

    toggle.addEventListener("change", () => {

        const newTheme = toggle.checked ? "dark" : "light";

        fetch("/profile/theme", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    theme: newTheme
                })
            })
            .then(r => r.json())
            .then(data => {

                if (data.success) {
                    showToast(`Switched to ${newTheme} mode`, "info");
                    applyTheme(newTheme);
                }
            });
    });
}

function applyTheme(theme) {

    if (theme === "light") {
        document.documentElement.style.setProperty("--bg", "#ffffff");
        document.documentElement.style.setProperty("--panel", "rgba(0,0,0,0.03)");
        document.documentElement.style.setProperty("--muted", "rgba(0,0,0,0.65)");
    } else {
        document.documentElement.style.setProperty("--bg", "#0b0c10");
        document.documentElement.style.setProperty("--panel", "rgba(255,255,255,0.07)");
        document.documentElement.style.setProperty("--muted", "rgba(255,255,255,0.75)");
    }
}

function initLimitForm() {

    const limitForm = document.getElementById("limitForm");
    if (!limitForm) return;

    limitForm.addEventListener("submit", (e) => {

        e.preventDefault();

        const formData = new FormData(limitForm);

        fetch("/profile/limit", {
                method: "POST",
                body: formData
            })
            .then(r => r.json())
            .then(data => {

                if (data.success) {
                    showToast("Monthly limits updated!", "success");

                    limitForm.querySelectorAll("input")
                        .forEach(i => flashUpdated(i));
                } else {
                    showToast(data.message || "Unable to update limit", "error");
                }
            });
    });
}

function flashUpdated(el) {
    el.classList.add("limit-updated");

    setTimeout(() => {
        el.classList.remove("limit-updated");
    }, 900);

    // Inject CSS once
    if (!document.getElementById("limitUpdatedStyles")) {
        const style = document.createElement("style");
        style.id = "limitUpdatedStyles";
        style.innerHTML = `
        .limit-updated {
            background: rgba(0,230,118,0.18) !important;
            box-shadow: 0 0 12px rgba(0,230,118,0.45);
            transition: all .4s ease;
        }
        `;
        document.head.appendChild(style);
    }
}

function switchSection(section) {

    document.querySelectorAll(".profile-section").forEach(sec => {
        sec.style.display = "none";
    });

    const active = document.getElementById(section);
    if (active) {
        active.style.display = "block";
        active.classList.add("visible");
    }
}
