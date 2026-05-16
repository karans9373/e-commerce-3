const state = {
  products: [],
  filteredProducts: [],
  selectedCategory: "All",
  maxPrice: 6000,
  search: "",
  sort: "default",
  cart: [],
  customer: JSON.parse(localStorage.getItem("customerAccount") || "null"),
};

const nav = document.getElementById("main-nav");
const menuToggle = nav ? document.querySelector(".menu-toggle") : null;
const year = document.getElementById("year");
const featuredProducts = document.getElementById("featured-products");
const childrenProducts = document.getElementById("children-products");
const shoesProducts = document.getElementById("shoes-products");
const watchesProducts = document.getElementById("watches-products");
const shopProducts = document.getElementById("shop-products");
const sortSelect = document.getElementById("sort-select");
const priceFilter = document.getElementById("price-filter");
const priceLabel = document.getElementById("price-label");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const cartButton = document.getElementById("cart-button");
const cartDrawer = document.getElementById("cart-drawer");
const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const cartCount = document.getElementById("cart-count");
const checkoutForm = document.getElementById("checkout-form");
const checkoutMessage = document.getElementById("checkout-message");
const ordersButton = document.getElementById("orders-button");
const customerButton = document.getElementById("customer-button");
const adminButton = document.getElementById("admin-button");
const orderLookupForm = document.getElementById("order-lookup-form");
const lookupEmail = document.getElementById("lookup-email");
const customerOrdersList = document.getElementById("customer-orders-list");
const productModal = document.getElementById("product-modal");
const productModalContent = document.getElementById("product-modal-content");
const customerModal = document.getElementById("customer-modal");
const customerLoginForm = document.getElementById("customer-login-form");
const customerSignupForm = document.getElementById("customer-signup-form");
const customerLoginMessage = document.getElementById("customer-login-message");
const customerSignupMessage = document.getElementById("customer-signup-message");
const fillCustomerDemo = document.getElementById("fill-customer-demo");
const backdrop = document.getElementById("global-backdrop");

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

if (menuToggle && nav) {
  menuToggle.addEventListener("click", () => nav.classList.toggle("open"));
}

if (year) {
  year.textContent = String(new Date().getFullYear());
}

document.querySelectorAll("[data-close-drawer]").forEach((button) => {
  button.addEventListener("click", closeDrawer);
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
  button.addEventListener("click", () => closeModal(button.dataset.closeModal));
});

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
    button.classList.add("active");
    state.selectedCategory = button.dataset.category || "All";
    applyFilters();
  });
});

document.querySelectorAll("[data-category-jump]").forEach((button) => {
  button.addEventListener("click", () => {
    const category = button.getAttribute("data-category-jump") || "All";
    const targetTab = document.querySelector(`.tab[data-category="${category}"]`);
    if (targetTab instanceof HTMLElement) {
      targetTab.click();
      document.getElementById("shop")?.scrollIntoView({ behavior: "smooth" });
    }
  });
});

if (sortSelect) {
  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    applyFilters();
  });
}

if (priceFilter && priceLabel) {
  priceFilter.addEventListener("input", () => {
    state.maxPrice = Number(priceFilter.value);
    priceLabel.textContent = `Up to ${formatCurrency(state.maxPrice)}`;
    applyFilters();
  });
}

if (searchForm && searchInput) {
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    state.search = searchInput.value.trim().toLowerCase();
    applyFilters();
    document.getElementById("shop")?.scrollIntoView({ behavior: "smooth" });
  });
}

if (cartButton) {
  cartButton.addEventListener("click", openDrawer);
}

if (ordersButton) {
  ordersButton.addEventListener("click", () => {
    document.getElementById("customer-orders")?.scrollIntoView({ behavior: "smooth" });
    lookupEmail?.focus();
  });
}

if (customerButton) {
  customerButton.addEventListener("click", () => openModal("customer-modal"));
}

if (adminButton) {
  adminButton.addEventListener("click", () => {
    window.open("/admin.html", "_blank", "noopener,noreferrer");
  });
}

if (checkoutForm) {
  checkoutForm.addEventListener("submit", submitOrder);
}

if (orderLookupForm) {
  orderLookupForm.addEventListener("submit", lookupOrders);
}

if (customerLoginForm) {
  customerLoginForm.addEventListener("submit", customerLogin);
}

if (customerSignupForm) {
  customerSignupForm.addEventListener("submit", customerSignup);
}

if (fillCustomerDemo) {
  fillCustomerDemo.addEventListener("click", async () => {
    const demo = await request("/api/customer/demo");
    document.getElementById("customer-login-email").value = demo.email;
    document.getElementById("customer-login-password").value = demo.password;
    document.getElementById("customer-signup-name").value = demo.name;
    document.getElementById("customer-signup-email").value = `${Date.now()}-${demo.email}`;
    document.getElementById("customer-signup-password").value = demo.password;
    document.getElementById("customer-signup-address").value = demo.address;
  });
}

if (backdrop) {
  backdrop.addEventListener("click", () => {
    closeDrawer();
    closeModal("product-modal");
    closeModal("customer-modal");
  });
}

async function request(url, options = {}) {
  const response = await fetch(url, {
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

function applyFilters() {
  let items = [...state.products].filter((product) => product.price <= state.maxPrice);
  if (state.selectedCategory !== "All") {
    items = items.filter((product) => product.category === state.selectedCategory);
  }
  if (state.search) {
    items = items.filter((product) => {
      const haystack = `${product.name} ${product.description} ${product.details} ${product.category}`.toLowerCase();
      return haystack.includes(state.search);
    });
  }
  if (state.sort === "name-asc") {
    items.sort((a, b) => a.name.localeCompare(b.name));
  } else if (state.sort === "name-desc") {
    items.sort((a, b) => b.name.localeCompare(a.name));
  } else if (state.sort === "price-asc") {
    items.sort((a, b) => a.price - b.price);
  } else if (state.sort === "price-desc") {
    items.sort((a, b) => b.price - a.price);
  }
  state.filteredProducts = items;
  renderProducts();
}

function createProductCard(product) {
  const card = document.createElement("article");
  card.className = "product-card clickable";
  card.innerHTML = `
    <img class="product-image product-photo" src="${product.image}" alt="${product.name}">
    <div class="product-meta">
      <p class="product-category">${product.category}</p>
      <h3>${product.name}</h3>
      <p>${product.description}</p>
      <div class="product-footer">
        <strong>${formatCurrency(product.price)}</strong>
        <span>Stock ${product.stock}</span>
      </div>
    </div>
  `;
  card.addEventListener("click", () => openProductModal(product.id));
  return card;
}

function renderProducts() {
  const featured = state.products.filter((product) => product.featured).slice(0, 10);
  featuredProducts.replaceChildren(...featured.map(createProductCard));
  renderCategoryShowcase(childrenProducts, "Children");
  renderCategoryShowcase(shoesProducts, "Shoes");
  renderCategoryShowcase(watchesProducts, "Watches");
  if (!state.filteredProducts.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state product-empty";
    empty.textContent = "No products match this filter right now.";
    shopProducts.replaceChildren(empty);
    return;
  }
  shopProducts.replaceChildren(...state.filteredProducts.map(createProductCard));
}

function renderCategoryShowcase(mountNode, category) {
  if (!mountNode) {
    return;
  }
  const items = state.products.filter((product) => product.category === category).slice(0, 4);
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = `No ${category.toLowerCase()} items available.`;
    mountNode.replaceChildren(empty);
    return;
  }
  mountNode.replaceChildren(...items.map(createProductCard));
}

function openDrawer() {
  cartDrawer.classList.add("open");
  cartDrawer.setAttribute("aria-hidden", "false");
  backdrop.classList.remove("hidden");
}

function closeDrawer() {
  cartDrawer.classList.remove("open");
  cartDrawer.setAttribute("aria-hidden", "true");
  if (!productModal.classList.contains("open") && !customerModal.classList.contains("open")) {
    backdrop.classList.add("hidden");
  }
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (!modal) {
    return;
  }
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  backdrop.classList.remove("hidden");
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (!modal) {
    return;
  }
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  if (!cartDrawer.classList.contains("open") && !productModal.classList.contains("open") && !customerModal.classList.contains("open")) {
    backdrop.classList.add("hidden");
  }
}

function updateCartCount() {
  cartCount.textContent = String(state.cart.reduce((sum, item) => sum + item.quantity, 0));
}

function renderCart() {
  updateCartCount();
  if (!state.cart.length) {
    cartItems.className = "drawer-body empty-state";
    cartItems.textContent = "Your cart is empty.";
    cartTotal.textContent = formatCurrency(0);
    return;
  }
  cartItems.className = "drawer-body";
  const rows = state.cart.map((item) => {
    const wrapper = document.createElement("div");
    wrapper.className = "cart-row";
    wrapper.innerHTML = `
      <div>
        <h4>${item.name}</h4>
        <p>${formatCurrency(item.price)} x ${item.quantity}</p>
      </div>
      <div class="cart-actions">
        <button type="button" data-cart-action="decrease">-</button>
        <span>${item.quantity}</span>
        <button type="button" data-cart-action="increase">+</button>
        <button type="button" data-cart-action="remove">Remove</button>
      </div>
    `;
    wrapper.querySelectorAll("button").forEach((button) => {
      button.addEventListener("click", () => {
        if (button.dataset.cartAction === "increase") {
          item.quantity += 1;
        } else if (button.dataset.cartAction === "decrease") {
          item.quantity = Math.max(1, item.quantity - 1);
        } else {
          state.cart = state.cart.filter((cartItem) => cartItem.id !== item.id);
        }
        renderCart();
      });
    });
    return wrapper;
  });
  cartItems.replaceChildren(...rows);
  cartTotal.textContent = formatCurrency(state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0));
}

async function openProductModal(productId) {
  try {
    const product = await request(`/api/products/${productId}`);
    productModalContent.innerHTML = `
      <div class="product-detail-grid">
        <img class="product-image detail-image product-photo" src="${product.image}" alt="${product.name}">
        <div>
          <p class="eyebrow">${product.category}</p>
          <h2>${product.name}</h2>
          <p>${product.details}</p>
          <p class="detail-price">${formatCurrency(product.price)}</p>
          <p>Available stock: ${product.stock}</p>
          <div class="detail-actions">
            <input id="modal-quantity" type="number" min="1" max="${product.stock}" value="1">
            <button type="button" class="cta" id="add-to-cart-button">Add to Cart</button>
          </div>
        </div>
      </div>
    `;
    document.getElementById("add-to-cart-button")?.addEventListener("click", () => {
      const quantity = Number(document.getElementById("modal-quantity")?.value || 1);
      addToCart(product, quantity);
      closeModal("product-modal");
      openDrawer();
    });
    openModal("product-modal");
  } catch (error) {
    console.error(error);
  }
}

function addToCart(product, quantity) {
  const existing = state.cart.find((item) => item.id === product.id);
  if (existing) {
    existing.quantity += quantity;
  } else {
    state.cart.push({ id: product.id, name: product.name, price: product.price, quantity });
  }
  renderCart();
}

async function submitOrder(event) {
  event.preventDefault();
  checkoutMessage.textContent = "";
  try {
    const payload = {
      customer: {
        name: document.getElementById("customer-name").value.trim(),
        email: document.getElementById("customer-email").value.trim(),
        address: document.getElementById("customer-address").value.trim(),
      },
      items: state.cart.map((item) => ({ id: item.id, quantity: item.quantity })),
    };
    const result = await request("/api/orders", { method: "POST", body: JSON.stringify(payload) });
    checkoutMessage.textContent = `Order #${result.order.id} placed successfully.`;
    state.cart = [];
    checkoutForm.reset();
    renderCart();
    hydrateCustomerFields();
    await loadProducts();
    lookupEmail.value = result.order.customer.email;
    await loadCustomerOrders(result.order.customer.email);
  } catch (error) {
    checkoutMessage.textContent = error.message;
  }
}

async function lookupOrders(event) {
  event.preventDefault();
  await loadCustomerOrders(lookupEmail.value.trim());
}

async function loadCustomerOrders(email) {
  if (!email) {
    customerOrdersList.className = "orders-list empty-state";
    customerOrdersList.textContent = "Enter an email to view your order updates.";
    return;
  }
  try {
    const result = await request(`/api/orders?email=${encodeURIComponent(email)}`);
    const orders = result.orders || [];
    if (!orders.length) {
      customerOrdersList.className = "orders-list empty-state";
      customerOrdersList.textContent = "No orders found for this email yet.";
      return;
    }
    customerOrdersList.className = "orders-list";
    customerOrdersList.replaceChildren(...orders.map(renderOrderCard));
  } catch (error) {
    customerOrdersList.className = "orders-list empty-state";
    customerOrdersList.textContent = error.message;
  }
}

function renderOrderCard(order) {
  const card = document.createElement("article");
  card.className = "order-card";
  const items = order.items.map((item) => `${item.name} x ${item.quantity}`).join(", ");
  card.innerHTML = `
    <div class="order-top">
      <h3>Order #${order.id}</h3>
      <span class="status-badge">${order.status}</span>
    </div>
    <p><strong>Date:</strong> ${order.createdAt}</p>
    <p><strong>Items:</strong> ${items}</p>
    <p><strong>Total:</strong> ${formatCurrency(order.total)}</p>
    <p><strong>Address:</strong> ${order.customer.address}</p>
  `;
  return card;
}

async function customerLogin(event) {
  event.preventDefault();
  customerLoginMessage.textContent = "";
  try {
    const result = await request("/api/customer/login", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("customer-login-email").value.trim(),
        password: document.getElementById("customer-login-password").value.trim(),
      }),
    });
    state.customer = result.customer;
    localStorage.setItem("customerAccount", JSON.stringify(state.customer));
    hydrateCustomerFields();
    customerLoginMessage.textContent = "Customer login successful.";
    customerButton.textContent = state.customer.name;
    closeModal("customer-modal");
  } catch (error) {
    customerLoginMessage.textContent = error.message;
  }
}

async function customerSignup(event) {
  event.preventDefault();
  customerSignupMessage.textContent = "";
  try {
    const result = await request("/api/customer/signup", {
      method: "POST",
      body: JSON.stringify({
        name: document.getElementById("customer-signup-name").value.trim(),
        email: document.getElementById("customer-signup-email").value.trim(),
        password: document.getElementById("customer-signup-password").value.trim(),
        address: document.getElementById("customer-signup-address").value.trim(),
      }),
    });
    state.customer = result.customer;
    localStorage.setItem("customerAccount", JSON.stringify(state.customer));
    hydrateCustomerFields();
    customerSignupMessage.textContent = "Signup complete.";
    customerButton.textContent = state.customer.name;
    closeModal("customer-modal");
  } catch (error) {
    customerSignupMessage.textContent = error.message;
  }
}

function hydrateCustomerFields() {
  if (!state.customer) {
    return;
  }
  document.getElementById("customer-name").value = state.customer.name || "";
  document.getElementById("customer-email").value = state.customer.email || "";
  document.getElementById("customer-address").value = state.customer.address || "";
  if (lookupEmail) {
    lookupEmail.value = state.customer.email || "";
  }
}

async function loadProducts() {
  try {
    const data = await request("/api/products");
    state.products = data.products || [];
    applyFilters();
  } catch (error) {
    console.error("Could not load product data.", error);
  }
}

renderCart();
loadProducts();
hydrateCustomerFields();
if (state.customer && customerButton) {
  customerButton.textContent = state.customer.name;
}
