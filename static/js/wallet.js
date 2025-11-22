document.addEventListener("DOMContentLoaded", () => {

    animateOnLoad(".wallet-header", 120);
    animateOnLoad(".balance-card", 150);
    animateOnLoad(".wallet-actions", 180);
    animateOnLoad(".history-card", 200);
    animateOnLoad(".history-item", 70);

    initDeposit();
    initWithdraw();
});

function animateOnLoad(selector, delay = 120) {
    document.querySelectorAll(selector).forEach((el, i) => {
        setTimeout(() => el.classList.add("visible"), i * delay);
    });
}

function initDeposit() {

    const depositBtn = document.getElementById("depositBtn");
    if (!depositBtn) return;

    depositBtn.addEventListener("click", () => openMoneyModal("deposit"));
}

function initWithdraw() {

    const withdrawBtn = document.getElementById("withdrawBtn");
    if (!withdrawBtn) return;

    withdrawBtn.addEventListener("click", () => openMoneyModal("withdraw"));
}

function openMoneyModal(type) {

    const modal = document.createElement("div");
    modal.className = "money-modal";

    const title = type === "deposit" ? "Deposit Money" : "Withdraw Money";
    const btnText = type === "deposit" ? "Deposit" : "Withdraw";

    modal.innerHTML = `
        <div class="money-box">
            <h3>${title}</h3>

            <input type="number" id="moneyInput" placeholder="Enter amount" min="1">

            <div class="money-actions">
                <button id="moneyConfirm" class="btn-primary">${btnText}</button>
                <button id="moneyCancel" class="btn-ghost">Cancel</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    setTimeout(() => modal.classList.add("visible"), 30);

    document.getElementById("moneyCancel").onclick = () => modal.remove();
    document.getElementById("moneyConfirm").onclick = () => processMoney(type, modal);
}

function processMoney(type, modal) {

    const amount = parseFloat(document.getElementById("moneyInput").value);

    if (!amount || amount <= 0) {
        return showToast("Enter a valid amount", "error");
    }

    fetch(`/wallet/${type}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount })
    })
    .then(r => r.json())
    .then(data => {

        if (!data.success) {
            showToast(data.message || "Transaction failed", "error");
            return;
        }

        showToast(type === "deposit" ? "Money added!" : "Money withdrawn!", "success");

        updateBalanceDisplay(data.new_balance);

        // Close modal with fade
        modal.classList.remove("visible");
        setTimeout(() => modal.remove(), 300);

        // Update history section
        if (data.history_item) {
            addHistoryItem(data.history_item);
        }
    });
}

function updateBalanceDisplay(newValue) {

    const el = document.getElementById("walletBalance");
    if (!el) return;

    animateNumber(el, newValue);

    el.classList.add("flash-green");
    setTimeout(() => el.classList.remove("flash-green"), 800);

    injectFlashStyles();
}

function animateNumber(el, newValue) {

    const start = parseFloat(el.innerText.replace(/[₹,]/g, "")) || 0;
    const duration = 1000;
    const startTime = performance.now();

    const update = (t) => {
        const progress = Math.min((t - startTime) / duration, 1);
        const value = start + (newValue - start) * progress;
        el.innerText = `₹${value.toFixed(2)}`;
        if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
}

function injectFlashStyles() {
    if (document.getElementById("walletFlashStyles")) return;

    const style = document.createElement("style");
    style.id = "walletFlashStyles";
    style.innerHTML = `
        .flash-green {
            color: rgb(0,230,118)!important;
            transition: color .5s ease;
        }
    `;
    document.head.appendChild(style);
}

function addHistoryItem(txn) {

    const list = document.getElementById("historyList");
    if (!list) return;

    const item = document.createElement("div");
    item.className = "history-item";

    item.innerHTML = `
        <div class="hist-info">
            <p class="merchant">${txn.merchant}</p>
            <p class="category">${txn.category}</p>
        </div>

        <div class="hist-meta">
            <p class="date">${txn.date}</p>
            <p class="amount ${txn.type === "expense" ? "red" : "green"}">
                ${txn.type === "expense" ? "-" : "+"} ₹${txn.amount}
            </p>
        </div>
    `;

    list.prepend(item);

    setTimeout(() => item.classList.add("visible"), 80);
}

(function injectModalStyles() {

    if (document.getElementById("moneyModalStyles")) return;

    const style = document.createElement("style");
    style.id = "moneyModalStyles";
    style.innerHTML = `
        .money-modal {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity .35s var(--easing);
            z-index: 9998;
        }
        .money-modal.visible {
            opacity: 1;
        }
        .money-box {
            background: rgba(255,255,255,0.07);
            padding: 28px;
            border-radius: 18px;
            width: 320px;
            backdrop-filter: blur(12px);
            box-shadow: 0 20px 45px rgba(0,0,0,0.55);
            text-align: center;
            color: white;
        }
        .money-actions {
            display: flex;
            gap: 14px;
            margin-top: 20px;
        }
        #moneyInput {
            margin-top: 14px;
            width: 100%;
            padding: 12px;
            border-radius: 12px;
            border: none;
            background: rgba(255,255,255,0.15);
            color:white;
            outline:none;
            font-size:1rem;
        }
    `;
    document.head.appendChild(style);
})();
