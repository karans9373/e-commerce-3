from __future__ import annotations

import json
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
ORDERS_FILE = DATA_DIR / "orders.json"
CUSTOMERS_FILE = DATA_DIR / "customers.json"
STATS_FILE = DATA_DIR / "stats.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_TOKEN = "ecommerce-admin-session"
DEMO_CUSTOMER_EMAIL = "customer@example.com"
DEMO_CUSTOMER_PASSWORD = "customer123"

DEFAULT_CUSTOMERS = [
    {
        "id": 1,
        "name": "Demo Customer",
        "email": DEMO_CUSTOMER_EMAIL,
        "password": DEMO_CUSTOMER_PASSWORD,
        "address": "221 Market Road, Mumbai, India",
    }
]

CATEGORY_CONFIG = [
    {
        "category": "Men",
        "base_names": [
            "Oxford Shirt", "Street Polo", "Urban Jacket", "Weekend Tee", "Tailored Kurta",
            "Denim Shirt", "Classic Hoodie", "Summer Linen", "Club Blazer", "Cargo Overshirt",
            "Festival Kurta", "Everyday Henley", "Retro Windbreaker", "Traveler Shirt", "Monsoon Layer",
            "Fitness Tee", "Checked Flannel", "Business Casual Shirt", "Textured Sweatshirt", "Signature Polo",
        ],
        "queries": [
            "men fashion shirt", "mens casual outfit", "men polo fashion", "male fashion portrait", "mens kurta style",
            "men denim outfit", "men hoodie fashion", "linen shirt men", "men blazer style", "men overshirt fashion",
            "indian men kurta fashion", "henley shirt men", "men windbreaker style", "traveler mens outfit", "mens layered outfit",
            "athletic tshirt men", "men flannel fashion", "business casual men", "mens sweatshirt fashion", "premium polo men",
        ],
        "tone": "blue",
        "featured": {0, 3, 8, 14},
        "price_start": 1499,
    },
    {
        "category": "Women",
        "base_names": [
            "Silk Top", "Corater Knit", "Studio Dress", "Bloom Jacket", "Velvet Kurti",
            "Classic Cardigan", "Runway Blouse", "City Co-ord", "Graceful Saree Set", "Pleated Skirt",
            "Weekend Shrug", "Pastel Hoodie", "Evening Tunic", "Soft Knitwear", "Boho Layer",
            "Holiday Dress", "Structured Blazer", "Flow Tee", "Cotton Kurta", "Contour Shirt",
        ],
        "queries": [
            "women fashion top", "women sweater fashion", "women dress fashion", "women jacket style", "women kurti fashion",
            "women cardigan style", "women blouse fashion", "women coord set", "saree fashion woman", "pleated skirt fashion",
            "women shrug fashion", "women pastel hoodie", "evening tunic women", "women knitwear style", "boho womens fashion",
            "holiday dress woman", "women blazer fashion", "women cotton tee", "women kurta style", "women shirt fashion",
        ],
        "tone": "pink",
        "featured": {1, 4, 7, 13},
        "price_start": 1699,
    },
    {
        "category": "Children",
        "base_names": [
            "Play Tee", "Rainbow Hoodie", "Tiny Jacket", "Star Shirt", "Happy Dress",
            "School Polo", "Comfy Shorts Set", "Little Kurta", "Sunny Outfit", "Mini Tracksuit",
            "Party Shirt", "Soft Pajama Set", "Weekend Frock", "Adventure Tee", "Layered Jacket",
            "Junior Sweatshirt", "Fun Co-ord", "Cartoon Tee", "Color Pop Hoodie", "Family Day Outfit",
        ],
        "queries": [
            "kids fashion tshirt", "kids hoodie fashion", "children jacket fashion", "kids shirt style", "girls dress fashion",
            "kids polo shirt", "kids shorts set", "kids kurta fashion", "children sunny outfit", "kids tracksuit style",
            "party shirt kids", "kids pajama fashion", "kids frock fashion", "children adventure outfit", "layered kids jacket",
            "kids sweatshirt fashion", "kids coord set", "cartoon tshirt kids", "kids colorful hoodie", "family day kids fashion",
        ],
        "tone": "green",
        "featured": {2, 5, 11, 16},
        "price_start": 999,
    },
    {
        "category": "Shoes",
        "base_names": [
            "Runner Pro", "City Sneakers", "Canvas Walk", "Trail Boost", "Leather Derby",
            "Sport Flex", "Classic Loafer", "Weekend Slip-On", "Street High Top", "Marathon Edge",
            "Training Pulse", "Heritage Brogue", "Urban Sandal", "Club Sneaker", "Storm Runner",
            "Minimal Trainer", "Retro Court", "Explorer Boot", "Daily Foam", "Velocity Knit",
        ],
        "queries": [
            "running shoes product", "sneakers fashion product", "canvas shoes product", "trail shoes product", "leather derby shoes",
            "sports shoes product", "loafer shoes product", "slip on shoes product", "high top sneakers", "marathon shoes product",
            "training sneakers product", "brogue shoes product", "fashion sandals product", "club sneaker product", "running shoes fashion",
            "minimal trainer shoes", "retro sneakers product", "boot shoes fashion", "foam runner shoes", "knit sneakers product",
        ],
        "tone": "coral",
        "featured": {0, 6, 10, 18},
        "price_start": 2199,
    },
    {
        "category": "Watches",
        "base_names": [
            "Chrono Steel", "Aura Watch", "Midnight Dial", "Vintage Strap", "Motion Quartz",
            "Sleek Smartwatch", "Classic Leather Time", "Pilot Edition", "Minimal Gold", "Ocean Blue Dial",
            "Executive Black", "Weekend Analog", "Rose Mesh", "Trail Watch", "Silver Edge",
            "Pulse Smart", "Night Navigator", "Modern Square", "Royal Strap", "Active Timepiece",
        ],
        "queries": [
            "wrist watch product", "fashion watch product", "black dial watch", "leather strap watch", "quartz watch product",
            "smartwatch product", "classic watch product", "pilot watch product", "gold watch product", "blue dial watch",
            "executive watch product", "analog watch product", "rose gold watch", "outdoor watch product", "silver watch product",
            "smart watch closeup", "night watch product", "square watch product", "strap watch fashion", "active watch product",
        ],
        "tone": "slate",
        "featured": {1, 8, 12, 19},
        "price_start": 2599,
    },
]

CATEGORY_IMAGE_POOLS = {
    "Men": [
        "https://images.pexels.com/photos/1212984/pexels-photo-1212984.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1300550/pexels-photo-1300550.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/936117/pexels-photo-936117.jpeg?auto=compress&cs=tinysrgb&w=900",
    ],
    "Women": [
        "https://images.pexels.com/photos/985635/pexels-photo-985635.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1462637/pexels-photo-1462637.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1036623/pexels-photo-1036623.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1758144/pexels-photo-1758144.jpeg?auto=compress&cs=tinysrgb&w=900",
        "https://images.pexels.com/photos/1381556/pexels-photo-1381556.jpeg?auto=compress&cs=tinysrgb&w=900",
    ],
    "Children": [
        "https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1514090458221-65bb69cf63e6?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?auto=format&fit=crop&w=900&q=80",
    ],
    "Shoes": [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1543508282-6319a3e2621f?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1514989940723-e8e51635b782?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=900&q=80",
    ],
    "Watches": [
        "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1434056886845-dac89ffe9b56?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1495856458515-0637185db551?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?auto=format&fit=crop&w=900&q=80",
    ],
}


def fashion_image(category: str, seed: int) -> str:
    pool = CATEGORY_IMAGE_POOLS.get(category, CATEGORY_IMAGE_POOLS["Men"])
    return pool[(seed - 1) % len(pool)]


def generate_catalog() -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    current_id = 1
    for category_index, config in enumerate(CATEGORY_CONFIG):
        for item_index, base_name in enumerate(config["base_names"]):
            products.append(
                {
                    "id": current_id,
                    "name": base_name,
                    "description": f"Premium {config['category'].lower()} collection piece with fresh styling.",
                    "details": f"{base_name} brings a polished {config['category'].lower()} look with strong visual identity, clean finishing, and all-day comfort for modern shoppers.",
                    "price": config["price_start"] + (item_index * 140) + (category_index * 60),
                    "category": config["category"],
                    "tone": config["tone"],
                    "featured": item_index in config["featured"],
                    "stock": 8 + ((item_index * 3 + category_index) % 21),
                    "image": fashion_image(config["category"], current_id),
                }
            )
            current_id += 1
    return products


def default_stats() -> dict[str, Any]:
    return {"total_visitors": 0, "daily_visitors": {}}


def ensure_data_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not PRODUCTS_FILE.exists():
        PRODUCTS_FILE.write_text(json.dumps(generate_catalog(), indent=2), encoding="utf-8")
    else:
        current_products = read_json(PRODUCTS_FILE, [])
        if len(current_products) < 100:
            PRODUCTS_FILE.write_text(json.dumps(generate_catalog(), indent=2), encoding="utf-8")
    if not ORDERS_FILE.exists():
        ORDERS_FILE.write_text("[]", encoding="utf-8")
    if not CUSTOMERS_FILE.exists():
        CUSTOMERS_FILE.write_text(json.dumps(DEFAULT_CUSTOMERS, indent=2), encoding="utf-8")
    if not STATS_FILE.exists():
        STATS_FILE.write_text(json.dumps(default_stats(), indent=2), encoding="utf-8")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def get_products() -> list[dict[str, Any]]:
    products = read_json(PRODUCTS_FILE, generate_catalog())
    changed = False
    for product in products:
        image = str(product.get("image", ""))
        category = str(product.get("category", "Men"))
        if (
            (not image)
            or ("source.unsplash.com" in image)
            or (category in {"Children", "Shoes", "Watches"} and "pexels.com" in image)
        ):
            product["image"] = fashion_image(category, int(product.get("id", 1)))
            changed = True
    if changed:
        save_products(products)
    return products


def save_products(products: list[dict[str, Any]]) -> None:
    write_json(PRODUCTS_FILE, products)


def get_orders() -> list[dict[str, Any]]:
    return read_json(ORDERS_FILE, [])


def save_orders(orders: list[dict[str, Any]]) -> None:
    write_json(ORDERS_FILE, orders)


def get_customers() -> list[dict[str, Any]]:
    return read_json(CUSTOMERS_FILE, DEFAULT_CUSTOMERS)


def save_customers(customers: list[dict[str, Any]]) -> None:
    write_json(CUSTOMERS_FILE, customers)


def get_stats() -> dict[str, Any]:
    return read_json(STATS_FILE, default_stats())


def save_stats(stats: dict[str, Any]) -> None:
    write_json(STATS_FILE, stats)


def next_id(items: list[dict[str, Any]]) -> int:
    if not items:
        return 1
    return max(int(item["id"]) for item in items) + 1


def money_total(items: list[dict[str, Any]]) -> float:
    return round(sum(float(item["price"]) * int(item["quantity"]) for item in items), 2)


def today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def track_visit() -> None:
    stats = get_stats()
    key = today_key()
    stats["total_visitors"] = int(stats.get("total_visitors", 0)) + 1
    daily = stats.get("daily_visitors", {})
    daily[key] = int(daily.get(key, 0)) + 1
    stats["daily_visitors"] = daily
    save_stats(stats)


def build_summary() -> dict[str, Any]:
    orders = get_orders()
    products = get_products()
    stats = get_stats()
    key = today_key()
    today_orders = [order for order in orders if str(order.get("createdAt", "")).startswith(key)]
    today_sales = round(sum(float(order["total"]) for order in today_orders), 2)
    category_counts: dict[str, int] = {}
    for product in products:
        category_counts[product["category"]] = category_counts.get(product["category"], 0) + 1
    return {
        "todaySales": today_sales,
        "todayOrders": len(today_orders),
        "visitorsToday": int(stats.get("daily_visitors", {}).get(key, 0)),
        "totalVisitors": int(stats.get("total_visitors", 0)),
        "productCount": len(products),
        "totalOrders": len(orders),
        "categoryCounts": category_counts,
    }


class EcommerceHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/products":
            self.send_json({"siteName": "E Commerce", "products": get_products()})
            return

        if path.startswith("/api/products/"):
            product_id = self.parse_int(path.rsplit("/", 1)[-1])
            product = next((item for item in get_products() if item["id"] == product_id), None)
            if not product:
                self.send_json({"error": "Product not found"}, status=404)
                return
            self.send_json(product)
            return

        if path == "/api/orders":
            query = parse_qs(parsed.query)
            email = (query.get("email") or [""])[0].strip().lower()
            orders = get_orders()
            if email:
                orders = [order for order in orders if order["customer"]["email"].lower() == email]
            self.send_json({"orders": orders})
            return

        if path == "/api/customer/demo":
            self.send_json(
                {
                    "name": "Demo Customer",
                    "email": DEMO_CUSTOMER_EMAIL,
                    "password": DEMO_CUSTOMER_PASSWORD,
                    "address": "221 Market Road, Mumbai, India",
                }
            )
            return

        if path == "/api/admin/products":
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.send_json({"products": get_products()})
            return

        if path == "/api/admin/orders":
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.send_json({"orders": get_orders()})
            return

        if path == "/api/admin/summary":
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.send_json(build_summary())
            return

        if path.startswith("/print/order/"):
            if not self.is_admin_request(parsed):
                self.send_html("<h1>Unauthorized</h1>", status=401)
                return
            order_id = self.parse_int(path.rsplit("/", 1)[-1])
            order = next((item for item in get_orders() if item["id"] == order_id), None)
            if not order:
                self.send_html("<h1>Order not found</h1>", status=404)
                return
            self.send_html(self.render_printable_order(order))
            return

        if path == "/":
            track_visit()
            self.path = "/index.html"
        elif path == "/index.html":
            track_visit()

        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        payload = self.read_body()

        if path == "/api/orders":
            self.handle_create_order(payload)
            return

        if path == "/api/admin/login":
            username = str(payload.get("username", "")).strip()
            password = str(payload.get("password", "")).strip()
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                self.send_json({"token": ADMIN_TOKEN, "username": ADMIN_USERNAME})
                return
            self.send_json({"error": "Invalid admin login"}, status=401)
            return

        if path == "/api/customer/signup":
            self.handle_customer_signup(payload)
            return

        if path == "/api/customer/login":
            self.handle_customer_login(payload)
            return

        if path == "/api/admin/products":
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.handle_create_product(payload)
            return

        if path.startswith("/api/admin/orders/") and path.endswith("/status"):
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            self.handle_update_order_status(path, payload)
            return

        self.send_json({"error": "Not found"}, status=404)

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/admin/products/"):
            if not self.is_admin_request(parsed):
                self.send_json({"error": "Unauthorized"}, status=401)
                return
            product_id = self.parse_int(path.rsplit("/", 1)[-1])
            products = get_products()
            next_products = [item for item in products if item["id"] != product_id]
            if len(next_products) == len(products):
                self.send_json({"error": "Product not found"}, status=404)
                return
            save_products(next_products)
            self.send_json({"ok": True})
            return

        self.send_json({"error": "Not found"}, status=404)

    def handle_create_order(self, payload: dict[str, Any]) -> None:
        customer = payload.get("customer") or {}
        cart_items = payload.get("items") or []

        name = str(customer.get("name", "")).strip()
        email = str(customer.get("email", "")).strip()
        address = str(customer.get("address", "")).strip()

        if not name or not email or not address:
            self.send_json({"error": "Customer name, email, and address are required."}, status=400)
            return

        if not cart_items:
            self.send_json({"error": "Your cart is empty."}, status=400)
            return

        products = get_products()
        products_by_id = {item["id"]: item for item in products}
        normalized_items: list[dict[str, Any]] = []

        for row in cart_items:
            product_id = self.parse_int(row.get("id"))
            quantity = max(1, self.parse_int(row.get("quantity"), default=1))
            product = products_by_id.get(product_id)
            if not product:
                self.send_json({"error": f"Product {product_id} not found."}, status=400)
                return
            if quantity > int(product["stock"]):
                self.send_json({"error": f"Only {product['stock']} left for {product['name']}."}, status=400)
                return
            normalized_items.append(
                {"id": product["id"], "name": product["name"], "price": product["price"], "quantity": quantity}
            )

        for item in normalized_items:
            products_by_id[item["id"]]["stock"] = int(products_by_id[item["id"]]["stock"]) - int(item["quantity"])

        updated_products = sorted(list(products_by_id.values()), key=lambda item: item["id"])
        save_products(updated_products)

        orders = get_orders()
        order = {
            "id": next_id(orders),
            "customer": {"name": name, "email": email, "address": address},
            "items": normalized_items,
            "total": money_total(normalized_items),
            "status": "Processing",
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        orders.insert(0, order)
        save_orders(orders)
        self.send_json({"ok": True, "order": order}, status=201)

    def handle_customer_signup(self, payload: dict[str, Any]) -> None:
        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip().lower()
        password = str(payload.get("password", "")).strip()
        address = str(payload.get("address", "")).strip()

        if not name or not email or not password or not address:
            self.send_json({"error": "All signup fields are required."}, status=400)
            return

        customers = get_customers()
        if any(customer["email"].lower() == email for customer in customers):
            self.send_json({"error": "Customer email already exists."}, status=400)
            return

        customer = {"id": next_id(customers), "name": name, "email": email, "password": password, "address": address}
        customers.append(customer)
        save_customers(customers)
        self.send_json({"ok": True, "customer": self.public_customer(customer)}, status=201)

    def handle_customer_login(self, payload: dict[str, Any]) -> None:
        email = str(payload.get("email", "")).strip().lower()
        password = str(payload.get("password", "")).strip()
        customer = next(
            (
                customer
                for customer in get_customers()
                if customer["email"].lower() == email and customer["password"] == password
            ),
            None,
        )
        if not customer:
            self.send_json({"error": "Invalid customer login."}, status=401)
            return
        self.send_json({"ok": True, "customer": self.public_customer(customer)})

    def handle_create_product(self, payload: dict[str, Any]) -> None:
        name = str(payload.get("name", "")).strip()
        description = str(payload.get("description", "")).strip()
        details = str(payload.get("details", "")).strip()
        category = str(payload.get("category", "Men")).strip() or "Men"
        tone = str(payload.get("tone", "blue")).strip() or "blue"
        price = float(payload.get("price", 0) or 0)
        stock = int(payload.get("stock", 0) or 0)
        featured = bool(payload.get("featured", False))
        image = str(payload.get("image", "")).strip()

        if not name or not description or not details or price <= 0 or stock < 0:
            self.send_json({"error": "Please fill all product fields with valid values."}, status=400)
            return

        products = get_products()
        product = {
            "id": next_id(products),
            "name": name,
            "description": description,
            "details": details,
            "price": round(price, 2),
            "category": category,
            "tone": tone,
            "featured": featured,
            "stock": stock,
            "image": image or fashion_image(category, next_id(products)),
        }
        products.append(product)
        save_products(products)
        self.send_json({"ok": True, "product": product}, status=201)

    def handle_update_order_status(self, path: str, payload: dict[str, Any]) -> None:
        order_id = self.parse_int(path.split("/")[-2])
        new_status = str(payload.get("status", "")).strip()
        valid = {"Processing", "Packed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"}
        if new_status not in valid:
            self.send_json({"error": "Invalid order status."}, status=400)
            return

        orders = get_orders()
        order = next((item for item in orders if item["id"] == order_id), None)
        if not order:
            self.send_json({"error": "Order not found"}, status=404)
            return

        order["status"] = new_status
        save_orders(orders)
        self.send_json({"ok": True, "order": order})

    def render_printable_order(self, order: dict[str, Any]) -> str:
        rows = "".join(
            f"<tr><td>{item['name']}</td><td>{item['quantity']}</td><td>&#8377;{item['price']}</td></tr>"
            for item in order["items"]
        )
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Order #{order['id']}</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 32px; color: #111; }}
    h1 {{ margin-bottom: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
    .meta {{ margin: 10px 0; color: #444; }}
  </style>
</head>
<body>
  <h1>Order #{order['id']}</h1>
  <div class="meta">Customer: {order['customer']['name']} ({order['customer']['email']})</div>
  <div class="meta">Address: {order['customer']['address']}</div>
  <div class="meta">Status: {order['status']}</div>
  <div class="meta">Placed: {order['createdAt']}</div>
  <table>
    <thead>
      <tr><th>Item</th><th>Quantity</th><th>Price</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <h3>Total: &#8377;{order['total']}</h3>
  <script>window.print()</script>
</body>
</html>"""

    def read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def parse_int(self, value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def is_admin_request(self, parsed: Any) -> bool:
        header_token = self.headers.get("X-Admin-Token", "")
        query_token = (parse_qs(parsed.query).get("token") or [""])[0]
        return header_token == ADMIN_TOKEN or query_token == ADMIN_TOKEN

    def public_customer(self, customer: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "address": customer["address"],
        }

    def send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, markup: str, status: int = 200) -> None:
        body = markup.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    ensure_data_files()
    server = ThreadingHTTPServer((host, port), EcommerceHandler)
    print(f"E Commerce running at http://{host}:{port}")
    print(f"Admin login -> username: {ADMIN_USERNAME} | password: {ADMIN_PASSWORD}")
    print(f"Demo customer -> email: {DEMO_CUSTOMER_EMAIL} | password: {DEMO_CUSTOMER_PASSWORD}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
