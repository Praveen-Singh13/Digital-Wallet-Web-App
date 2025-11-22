document.addEventListener("DOMContentLoaded", () => {

    animateOnLoad(".summary-card", 120);
    animateOnLoad(".graph-card", 150);
    animateOnLoad(".recent-card", 180);
    animateOnLoad(".txn-item", 80);
    animateOnLoad(".dashboard-header", 80);

    initDashboardCharts();
});

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}

function initDashboardCharts() {

    const monthlyCtx = document.getElementById("dashboardMonthlyChart");
    const categoryCtx = document.getElementById("dashboardCategoryChart");

    if (!monthlyCtx || !categoryCtx) return;

    new Chart(monthlyCtx, {
        type: "line",
        data: dashboardMonthlyData,
        options: {
            animation: {
                duration: 1400,
                easing: "easeInOutQuart"
            },
            tension: 0.35,
            responsive: true,
            scales: {
                y: {
                    grid: {
                        color: "rgba(255,255,255,0.04)"
                    },
                    ticks: {
                        color: "#fff"
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: "#fff"
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#fff"
                    }
                },
                tooltip: {
                    backgroundColor: "rgba(10,10,20,0.95)",
                    bodyColor: "#fff"
                }
            }
        }
    });

    new Chart(categoryCtx, {
        type: "doughnut",
        data: dashboardCategoryData,
        options: {
            responsive: true,
            cutout: "60%",
            animation: {
                duration: 1500,
                easing: "easeOutCubic"
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#fff"
                    }
                },
                tooltip: {
                    backgroundColor: "rgba(10,10,20,0.95)"
                }
            }
        }
    });
}

function animateNumber(el, newValue) {
    const start = parseFloat(el.innerText.replace(/[₹,]/g, "")) || 0;
    const duration = 900;
    const startTime = performance.now();

    const update = (now) => {
        const progress = Math.min((now - startTime) / duration, 1);
        const value = start + (newValue - start) * progress;

        el.innerText = `₹${value.toFixed(2)}`;

        if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
}

function refreshDashboard() {

    fetch("/dashboard/data")
        .then(res => res.json())
        .then(data => {
            if (!data.success) return;

            // Update numbers
            animateNumber(document.getElementById("db_total_balance"), data.totalBalance);
            animateNumber(document.getElementById("db_total_spent"), data.totalSpent);
            animateNumber(document.getElementById("db_net_amount"), data.net);

            // Refresh charts
            initDashboardCharts();
        });
}

function flashValue(el, type = "green") {
    el.classList.add(`flash-${type}`);
    setTimeout(() => el.classList.remove(`flash-${type}`), 700);
}

(function injectFlashStyles() {
    if (document.getElementById("flashStyles")) return;

    const style = document.createElement("style");
    style.id = "flashStyles";
    style.innerHTML = `
        .flash-green { color: rgb(0,230,118) !important; transition: color .5s ease; }
        .flash-red   { color: rgb(255,82,82) !important; transition: color .5s ease; }
    `;
    document.head.appendChild(style);
})();

function scrollToTxns() {
    document.getElementById("recentTransactions")?.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}
