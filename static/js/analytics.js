document.addEventListener("DOMContentLoaded", () => {

    animateOnLoad(".glass-card", 120);
    animateOnLoad(".alert", 80);
    animateOnLoad(".page-header", 80);

    loadCharts();
    loadInsights();
});

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}

function loadCharts() {
    const lineCtx = document.getElementById("monthlyChart");
    const pieCtx = document.getElementById("categoryChart");
    const barCtx = document.getElementById("yearlyChart");

    if (!lineCtx || !pieCtx || !barCtx) return;

    new Chart(lineCtx, {
        type: "line",
        data: monthlyData,
        options: {
            responsive: true,
            animation: {
                duration: 1500,
                easing: "easeInOutQuart"
            },
            tension: 0.35,
            scales: {
                y: {
                    ticks: {
                        color: "#fff"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.05)"
                    }
                },
                x: {
                    ticks: {
                        color: "#fff"
                    },
                    grid: {
                        display: false
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
                    backgroundColor: "rgba(8,8,10,0.95)",
                    titleColor: "#fff",
                    bodyColor: "#fff"
                }
            }
        }
    });

    new Chart(pieCtx, {
        type: "doughnut",
        data: categoryData,
        options: {
            responsive: true,
            cutout: "55%",
            animation: {
                duration: 1600,
                easing: "easeOutCubic"
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#fff"
                    }
                },
                tooltip: {
                    backgroundColor: "rgba(8,8,10,0.95)",
                    bodyColor: "#fff"
                }
            }
        }
    });

    new Chart(barCtx, {
        type: "bar",
        data: yearData,
        options: {
            responsive: true,
            animation: {
                duration: 1500,
                easing: "easeInOutExpo"
            },
            scales: {
                y: {
                    ticks: {
                        color: "#fff"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.05)"
                    }
                },
                x: {
                    ticks: {
                        color: "#fff"
                    },
                    grid: {
                        display: false
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
                    backgroundColor: "rgba(8,8,10,0.95)",
                    bodyColor: "#fff"
                }
            }
        }
    });
}

function loadInsights() {
    fetch("/analytics/insights")
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;

            renderInsights(data.insights);
        })
        .catch(err => console.error("Analytics insights error:", err));
}

function renderInsights(list) {
    const container = document.getElementById("insightContainer");
    if (!container) return;

    container.innerHTML = "";

    list.forEach((insight, i) => {
        const item = document.createElement("div");
        item.className = `alert alert-${insight.type}`;
        item.innerText = insight.message;

        container.appendChild(item);

        setTimeout(() => item.classList.add("visible"), i * 120);
    });
}

function refreshAnalytics() {

    fetch("/analytics/data")
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;

            // Animate numbers
            animateNumber(document.getElementById("totalSpent"), data.totalSpent);
            animateNumber(document.getElementById("totalIncome"), data.totalIncome);
            animateNumber(document.getElementById("netBalance"), data.netBalance);

            loadCharts();
        });
}

function animateNumber(el, newValue) {
    const start = parseFloat(el.innerText.replace(/[₹,]/g, "")) || 0;
    const duration = 900;
    const startTime = performance.now();

    function update(time) {
        const progress = Math.min((time - startTime) / duration, 1);
        const value = start + (newValue - start) * progress;
        el.innerText = `₹${value.toFixed(2)}`;

        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}

function scrollToSection(id) {
    document.getElementById(id)?.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}
