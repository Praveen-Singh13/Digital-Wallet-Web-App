document.addEventListener("DOMContentLoaded", () => {

    animateOnLoad(".filter-card", 120);
    animateOnLoad(".txn-list-card", 150);
    animateOnLoad(".txn-item", 100);
    animateOnLoad(".page-header", 120);

    initFilters();
});

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}

function initFilters() {

    const btn = document.getElementById("applyFilters");
    if (!btn) return;

    btn.addEventListener("click", () => applyFilters());
}

function applyFilters() {

    const params = new URLSearchParams({
        category: document.getElementById("filterCategory")?.value || "",
        month: document.getElementById("filterMonth")?.value || "",
        year: document.getElementById("filterYear")?.value || "",
        merchant: document.getElementById("filterMerchant")?.value || "",
    });

    const list = document.getElementById("txnList");
    if (!list) return;

    list.innerHTML = `
        <div class="shimmer" style="height:18px;"></div>
        <div class="shimmer" style="height:18px; margin-top:10px;"></div>
        <div class="shimmer" style="height:18px; margin-top:10px;"></div>
    `;

    fetch(`/transactions/filter?${params}`)
        .then(r => r.json())
        .then(data => {

            if (!data.success) {
                list.innerHTML = "<p>No transactions found.</p>";
                return;
            }

            renderTransactions(data.transactions);
        });
}

function renderTransactions(listData) {

    const container = document.getElementById("txnList");
    if (!container) return;

    container.innerHTML = "";

    listData.forEach((t, i) => {

        const item = document.createElement("div");
        item.className = "txn-item";

        item.setAttribute("data-id", t.id);

        item.innerHTML = `
            <div class="txn-info">
                <p class="merchant">${t.merchant}</p>
                <p class="category">${t.category || "Uncategorized"}</p>
            </div>

            <div class="txn-meta">
                <p class="date">${t.date}</p>
            </div>

            <div class="txn-actions">
                <p class="amount ${t.type === "expense" ? "red" : "green"}">
                    ${t.type === "expense" ? "-" : "+"} ₹${t.amount}
                </p>

                <a href="/transactions/edit/${t.id}" class="edit-btn hover-glow">
                    <i class="fas fa-edit"></i>
                </a>

                <button class="delete-btn hover-glow" onclick="deleteTransaction(${t.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        container.appendChild(item);

        setTimeout(() => item.classList.add("visible"), i * 80);
    });
}

function deleteTransaction(id) {

    confirmAction("Delete this transaction?", (yes) => {

        if (!yes) return;

        fetch(`/transactions/delete/${id}`, {
                method: "POST"
            })
            .then(r => r.json())
            .then(data => {

                if (!data.success) return showToast("Delete failed", "error");

                const item = document.querySelector(`[data-id="${id}"]`);

                if (item) {
                    item.style.opacity = "0";
                    item.style.transform = "translateY(15px)";
                    setTimeout(() => item.remove(), 350);
                }

                showToast("Transaction deleted", "success");
            });
    });
}

function updateWalletBalance(newValue) {

    const balanceEl = document.getElementById("walletBalance");
    if (!balanceEl) return;

    animateNumber(balanceEl, newValue);

    balanceEl.classList.add("flash-green");
    setTimeout(() => balanceEl.classList.remove("flash-green"), 600);
}

function animateNumber(el, newValue) {
    const start = parseFloat(el.innerText.replace(/[₹,]/g, "")) || 0;
    const duration = 900;
    const startTime = performance.now();

    const update = (time) => {
        const progress = Math.min((time - startTime) / duration, 1);
        const value = start + (newValue - start) * progress;

        el.innerText = `₹${value.toFixed(2)}`;

        if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
}
