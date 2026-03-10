const API_KEY = "secret";

async function loadStats() {
  const res = await fetch("/api/orders/stats");
  const data = await res.json();
  document.getElementById("stats-total").textContent = data.total;
  document.getElementById("stats-revenue").textContent = "$" + data.revenue.toFixed(2);
  document.getElementById("stats-pending").textContent = data.by_status.pending ?? 0;
  document.getElementById("stats-fulfilled").textContent = data.by_status.fulfilled ?? 0;
  document.getElementById("stats-cancelled").textContent = data.by_status.cancelled ?? 0;
}

async function loadOrders() {
  const status = document.getElementById("status-filter").value;
  const url = status ? `/api/orders?status=${encodeURIComponent(status)}` : "/api/orders";
  const res = await fetch(url);
  const data = await res.json();
  const tbody = document.getElementById("orders-body");
  tbody.innerHTML = "";
  data.orders.forEach(o => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${o.customer}</td>
      <td>${o.item}</td>
      <td>${o.quantity}</td>
      <td>${o.price.toFixed(2)}</td>
      <td>${o.status}</td>
      <td>${new Date(o.created_at).toLocaleString()}</td>
      <td><button class="del-btn" data-id="${o.id}">Delete</button></td>
    `;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll(".del-btn").forEach(btn => {
    btn.addEventListener("click", () => deleteOrder(btn.dataset.id));
  });
  await loadStats();
}

async function deleteOrder(id) {
  await fetch(`/api/orders/${id}`, {
    method: "DELETE",
    headers: { "X-API-Key": API_KEY },
  });
  await loadOrders();
}

document.getElementById("status-filter").addEventListener("change", loadOrders);

document.getElementById("order-form").addEventListener("submit", async e => {
  e.preventDefault();
  const errEl = document.getElementById("error-msg");
  errEl.textContent = "";
  const body = {
    customer: document.getElementById("customer").value,
    item: document.getElementById("item").value,
    quantity: parseInt(document.getElementById("quantity").value, 10),
    price: parseFloat(document.getElementById("price").value),
  };
  const res = await fetch("/api/orders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json();
    errEl.textContent = err.error || "Failed to create order.";
    return;
  }
  e.target.reset();
  await loadOrders();
});

loadOrders();
