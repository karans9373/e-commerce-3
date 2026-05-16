const adminState = {
  token: localStorage.getItem("adminToken") || "",
};
const API_BASE = window.APP_CONFIG?.API_BASE || "";

const loginForm = document.getElementById("admin-login-form");
const loginMessage = document.getElementById("admin-login-message");
const fillAdminDemo = document.getElementById("fill-admin-demo");
const adminPanel = document.getElementById("admin-panel");
const statsGrid = document.getElementById("stats-grid");
const adminProducts = document.getElementById("admin-products");
const adminOrders = document.getElementById("admin-orders");
const addProductForm = document.getElementById("add-product-form");
const addProductMessage = document.getElementById("add-product-message");
const appLoader = document.getElementById("app-loader");
const loaderText = document.getElementById("loader-text");

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function showLoader(message = "Loading...") {
  if (loaderText) {
    loaderText.textContent = message;
  }
  appLoader?.classList.remove("hidden");
}

function hideLoader() {
  appLoader?.classList.add("hidden");
}

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

if (fillAdminDemo) {
  fillAdminDemo.addEventListener("click", () => {
    document.getElementById("admin-username").value = "admin";
    document.getElementById("admin-password").value = "admin123";
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    loginMessage.textContent = "";
    showLoader("Logging in and loading dashboard data.");
    try {
      const result = await request("/api/admin/login", {
        method: "POST",
        body: JSON.stringify({
          username: document.getElementById("admin-username").value.trim(),
          password: document.getElementById("admin-password").value.trim(),
        }),
      });
      adminState.token = result.token;
      localStorage.setItem("adminToken", adminState.token);
      loginMessage.textContent = "Admin login successful.";
      adminPanel.classList.remove("hidden");
      await loadDashboard();
      hideLoader();
    } catch (error) {
      loginMessage.textContent = error.message;
      showLoader("Dashboard could not load. Please check backend status or try again.");
    }
  });
}

if (addProductForm) {
  addProductForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    addProductMessage.textContent = "";
    try {
      await request("/api/admin/products", {
        method: "POST",
        headers: { "X-Admin-Token": adminState.token },
        body: JSON.stringify({
          name: document.getElementById("new-name").value.trim(),
          description: document.getElementById("new-description").value.trim(),
          details: document.getElementById("new-details").value.trim(),
          price: Number(document.getElementById("new-price").value),
          stock: Number(document.getElementById("new-stock").value),
          category: document.getElementById("new-category").value,
          tone: document.getElementById("new-tone").value,
          featured: document.getElementById("new-featured").checked,
          image: document.getElementById("new-image").value.trim(),
        }),
      });
      addProductForm.reset();
      addProductMessage.textContent = "Product listed successfully.";
      await loadDashboard();
    } catch (error) {
      addProductMessage.textContent = error.message;
    }
  });
}

function renderStats(summary) {
  const cards = [
    { label: "Sales Today", value: formatCurrency(summary.todaySales), tone: "sales" },
    { label: "Visitors Today", value: String(summary.visitorsToday), tone: "visitors" },
    { label: "Orders Today", value: String(summary.todayOrders), tone: "orders" },
    { label: "Total Products", value: String(summary.productCount), tone: "products" },
  ];
  statsGrid.replaceChildren(...cards.map((card) => {
    const node = document.createElement("article");
    node.className = `stat-card ${card.tone}`;
    node.innerHTML = `<p>${card.label}</p><strong>${card.value}</strong>`;
    return node;
  }));
}

function renderProducts(products) {
  if (!products.length) {
    adminProducts.className = "admin-list empty-state";
    adminProducts.textContent = "No products available.";
    return;
  }
  adminProducts.className = "admin-list";
  adminProducts.replaceChildren(...products.map((product) => {
    const card = document.createElement("div");
    card.className = "admin-row rich";
    card.innerHTML = `
      <img src="${product.image}" alt="${product.name}">
      <div>
        <h4>${product.name}</h4>
        <p>${product.category} | ${formatCurrency(product.price)} | Stock ${product.stock}</p>
      </div>
      <button type="button" class="ghost-button danger">Remove</button>
    `;
    card.querySelector("button").addEventListener("click", async () => {
      await request(`/api/admin/products/${product.id}`, {
        method: "DELETE",
        headers: { "X-Admin-Token": adminState.token },
      });
      await loadDashboard();
    });
    return card;
  }));
}

function renderOrders(orders) {
  if (!orders.length) {
    adminOrders.className = "admin-list empty-state";
    adminOrders.textContent = "No orders yet.";
    return;
  }
  adminOrders.className = "admin-list";
  adminOrders.replaceChildren(...orders.map((order) => {
    const card = document.createElement("div");
    card.className = "admin-order-card rich";
    const options = ["Processing", "Packed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"]
      .map((status) => `<option value="${status}" ${status === order.status ? "selected" : ""}>${status}</option>`)
      .join("");
    const items = order.items.map((item) => `${item.name} x ${item.quantity}`).join(", ");
    card.innerHTML = `
      <div class="admin-order-top">
        <div>
          <h4>Order #${order.id}</h4>
          <p>${order.customer.name} | ${order.customer.email}</p>
          <p>${items}</p>
          <p>Total ${formatCurrency(order.total)}</p>
        </div>
        <div class="order-tools stacked">
          <select>${options}</select>
          <button type="button" class="ghost-button update-order">Update</button>
          <button type="button" class="ghost-button print-order">Print</button>
        </div>
      </div>
    `;
    const select = card.querySelector("select");
    card.querySelector(".update-order").addEventListener("click", async () => {
      await request(`/api/admin/orders/${order.id}/status`, {
        method: "POST",
        headers: { "X-Admin-Token": adminState.token },
        body: JSON.stringify({ status: select.value }),
      });
      await loadDashboard();
    });
    card.querySelector(".print-order").addEventListener("click", () => {
      window.open(`${API_BASE}/print/order/${order.id}?token=${encodeURIComponent(adminState.token)}`, "_blank");
    });
    return card;
  }));
}

async function loadDashboard() {
  showLoader("Connecting to backend and preparing admin data.");
  const [summary, productsResult, ordersResult] = await Promise.all([
    request("/api/admin/summary", { headers: { "X-Admin-Token": adminState.token } }),
    request("/api/admin/products", { headers: { "X-Admin-Token": adminState.token } }),
    request("/api/admin/orders", { headers: { "X-Admin-Token": adminState.token } }),
  ]);
  renderStats(summary);
  renderProducts(productsResult.products || []);
  renderOrders(ordersResult.orders || []);
  hideLoader();
}

if (adminState.token) {
  adminPanel.classList.remove("hidden");
  loadDashboard().catch((error) => {
    loginMessage.textContent = error.message;
    showLoader("Dashboard could not load. Please check backend status or try again.");
  });
} else {
  hideLoader();
}
