document.addEventListener("DOMContentLoaded", () => {

    initSidebar();
    revealOnScroll();
    autoAnimatePageLoad();
});

function autoAnimatePageLoad() {
    animateOnLoad(".glass-card", 120);
    animateOnLoad(".page-header", 120);
    animateOnLoad(".fade-in", 100);
    animateOnLoad(".fade-up", 120);
    animateOnLoad(".slide-down", 150);
}

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}


function initSidebar() {

    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const toggleBtn = document.getElementById("sidebarToggle");

    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        overlay.classList.toggle("visible");

        if (sidebar.classList.contains("open")) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "auto";
        }
    });

    overlay?.addEventListener("click", () => {
        sidebar.classList.remove("open");
        overlay.classList.remove("visible");
        document.body.style.overflow = "auto";
    });
}

function revealOnScroll() {

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });

    }, {
        threshold: 0.15
    });

    document.querySelectorAll(".reveal, .glass-card, .fade-in, .fade-up")
        .forEach(el => observer.observe(el));
}

function showToast(message, type = "info") {

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("visible");
    }, 50);

    setTimeout(() => {
        toast.classList.remove("visible");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

(function injectToastStyles() {
    if (document.getElementById("toastStyles")) return;

    const style = document.createElement("style");
    style.id = "toastStyles";
    style.innerHTML = `
        .toast {
            position: fixed;
            left: 50%;
            bottom: 35px;
            transform: translateX(-50%) translateY(20px);
            padding: 12px 20px;
            background: rgba(0,0,0,0.75);
            color: white;
            border-radius: 12px;
            opacity: 0;
            font-weight: 600;
            z-index: 9999;
            transition: all .35s var(--easing);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .toast.visible {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        .toast-info { background: rgba(108,99,255,.85); }
        .toast-success { background: rgba(0,230,118,.85); }
        .toast-error { background: rgba(255,82,82,.85); }
    `;
    document.head.appendChild(style);
})();

function scrollToElement(id) {
    document.getElementById(id)?.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

document.addEventListener("focusin", e => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT") {
        e.target.classList.add("focus-active");
    }
});
document.addEventListener("focusout", e => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT") {
        e.target.classList.remove("focus-active");
    }
});

(function injectFocusStyles() {
    if (document.getElementById("focusStyles")) return;

    const style = document.createElement("style");
    style.id = "focusStyles";
    style.innerHTML = `
        .focus-active {
            transform: translateY(-2px) !important;
            background: rgba(255,255,255,0.18) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.35) !important;
        }
    `;
    document.head.appendChild(style);
})();

function confirmAction(message, callback) {

    const modal = document.createElement("div");
    modal.className = "confirm-modal";

    modal.innerHTML = `
        <div class="confirm-box">
            <p>${message}</p>
            <div class="actions">
                <button id="confirmYes" class="btn-primary">Yes</button>
                <button id="confirmNo" class="btn-ghost">Cancel</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    setTimeout(() => modal.classList.add("visible"), 50);

    document.getElementById("confirmYes").onclick = () => {
        callback(true);
        modal.remove();
    };
    document.getElementById("confirmNo").onclick = () => {
        callback(false);
        modal.remove();
    };
}

(function injectModalStyles() {
    if (document.getElementById("modalStyles")) return;

    const style = document.createElement("style");
    style.id = "modalStyles";
    style.innerHTML = `
        .confirm-modal {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            z-index: 9998;
            transition: opacity .35s var(--easing);
        }
        .confirm-modal.visible {
            opacity: 1;
        }
        .confirm-box {
            background: rgba(255,255,255,0.07);
            padding: 26px;
            border-radius: 16px;
            backdrop-filter: blur(14px);
            box-shadow: 0 20px 45px rgba(0,0,0,0.55);
            width: 320px;
            text-align: center;
            color: white;
        }
        .actions {
            display: flex;
            gap: 14px;
            margin-top: 18px;
        }
    `;
    document.head.appendChild(style);
})();
