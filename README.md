# ShopEasy — E-Commerce Shopping Platform

**Task ID:** PY-EC-001 · Free Python Full Stack Internship
**Stack:** Django 4.2 · MySQL 8 · Django REST Framework · Bootstrap 5

A complete, working e-commerce web application: product catalog with search/filter,
shopping cart, checkout, order management, a Django admin dashboard, a demo Razorpay
payment flow, and a wishlist — built entirely with the Django ORM, MySQL-ready.

---

## 0. Quick Start (easiest way to run this — no MySQL needed)

This project runs on **SQLite by default**, so there is nothing to install or
configure beyond Python itself. One script does everything: creates a virtual
environment, installs dependencies, sets up the database, adds sample products,
and starts the server.

**Requirement:** Python 3.8+ installed ([download here](https://www.python.org/downloads/) —
on Windows, tick "Add Python to PATH" during install).

### Windows
Double-click **`run_windows.bat`** (or open a terminal in the project folder and run `run_windows.bat`).

### Mac / Linux
```bash
./run_mac_linux.sh
```
(If you get a permission error: `chmod +x run_mac_linux.sh` then run it again.)

Either script will open the app at **http://127.0.0.1:8000/**. Log in with:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@12345` |
| Customer | `testuser` | `Test@12345` |

Press `Ctrl+C` in the terminal to stop the server. Run the same script again any
time to restart it — it won't reinstall or reseed anything that's already there.

**Prefer to do it manually / already have a venv workflow?**
```bash
python manage.py migrate
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Once you're comfortable with SQLite and want to switch to MySQL (e.g. for your
final submission, since the task specifies MySQL), see **Section 4** below —
it's a two-line environment variable change.

---

## 1. Features Implemented

| Feature | Status | Notes |
|---|---|---|
| User Authentication | ✅ | Register, login, logout, profile edit, password change/reset — all via Django's built-in `auth` |
| Product Catalog | ✅ | Categories, search, price/category filters, sorting, pagination |
| Shopping Cart | ✅ | Session-based (works for guests too), add/update/remove, live totals |
| Checkout Process | ✅ | Shipping address form, COD or Online payment method, order summary |
| Order Management | ✅ | Order history, order detail, status timeline, cancel order (restocks items) |
| Admin Dashboard | ✅ | Django admin for categories, products (+ image gallery inline), orders (+ line items & status history inline), reviews, payments |
| Payment Integration | ✅ | Razorpay flow wired end-to-end; runs in **demo mode** out of the box, live-mode code included but commented (see §5) |
| Wishlist | ✅ | Add/remove from product page or listing, dedicated wishlist page |
| REST API | ➕ Bonus | Read-only DRF endpoints for products & categories at `/api/` |

---

## 2. Project Structure

```
ecommerce_project/      Django project settings, root urls.py, wsgi/asgi
accounts/                Profile model, auth views (register/login/profile)
catalog/                 Category, Product, Review models + storefront views + REST API
cart/                     Session-based cart logic
orders/                   Order, OrderItem, OrderStatusHistory + checkout flow
payments/                 Payment model + Razorpay integration (demo + live-mode code)
wishlist/                 Wishlist model + views
templates/                All HTML templates (Bootstrap 5)
static/css/style.css      Custom theme
media/                    Uploaded product images / avatars (created at runtime)
requirements.txt
.env.example
manage.py
```

---

## 3. Prerequisites

- Python 3.8+
- MySQL Server 8.x, running locally (or a remote MySQL instance)
- pip / virtualenv
- (Optional) MySQL Workbench, for inspecting the database visually

---

## 4. Switching to MySQL

The app runs on SQLite by default so it works instantly. Since the task requires
MySQL, switch over once you're ready to finalize your submission:

### Step 1 — Extract & create a virtual environment
```bash
cd ecommerce_project_root
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 1 — Extract & create a virtual environment
```bash
cd ecommerce_project_root
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Create the MySQL database
Open MySQL Workbench or the `mysql` CLI and run:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 3 — Configure environment variables
Copy `.env.example` to `.env` (or just export the variables in your shell / set them
in your hosting panel) and fill in your DB credentials:
```bash
cp .env.example .env
```
Key variables:
```
DB_ENGINE=mysql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```
> **Quick demo without MySQL?** Set `DB_ENGINE=sqlite` and skip straight to Step 4 —
> the project will use a local `db.sqlite3` file instead. Useful for a fast first run;
> switch back to `mysql` for your actual submission/demo.

### Step 4 — Migrate & seed sample data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data      # creates sample categories/products + demo accounts
```
`seed_data` creates:
- Superuser: **admin / Admin@12345**
- Demo customer: **testuser / Test@12345**
- 5 categories, ~28 sample products with prices, stock, and discounts
- A generated placeholder photo for every product and category (colored image with
  the product name on it), so the storefront shows real images instead of "No Image"
  boxes out of the box. Replace them anytime with real photos via the admin dashboard
  (Products → edit → upload an image).

(Skip `seed_data` and run `python manage.py createsuperuser` instead if you'd rather
start with an empty catalog and add products yourself through the admin.)

### Step 5 — Run the development server
```bash
python manage.py runserver
```
Visit:
- Storefront: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/admin/
- REST API: http://127.0.0.1:8000/api/products/

---

## 5. Payment Integration (Razorpay)

The checkout → payment flow is fully wired in `payments/views.py`. Out of the box it
runs in **demo mode**: choosing "Online Payment" at checkout takes you to a payment
page that simulates a successful Razorpay transaction (no real card/UPI details, no
external network call) — this lets you demo and test the complete order lifecycle
without a Razorpay account.

To accept **real test payments**:
1. Create a free account at https://dashboard.razorpay.com and grab your **Test**
   API Key ID & Secret (Settings → API Keys).
2. `pip install razorpay` and add `razorpay==1.4.2` to `requirements.txt`.
3. Set `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` in your `.env`.
4. In `payments/views.py`, uncomment the **LIVE MODE** blocks in `initiate_payment()`
   and `payment_success()` (they create a real Razorpay order and verify the payment
   signature server-side).
5. Load the Razorpay Checkout.js script in `templates/payments/payment_page.html`
   and replace the demo "Pay Now" form with the real Checkout widget (Razorpay's
   docs have a copy-paste snippet for this: https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/).

Cash on Delivery (`cod`) requires no configuration and works immediately.

---

## 6. Default Test Accounts (after `seed_data`)

| Role | Username | Password |
|---|---|---|
| Admin / Staff | `admin` | `Admin@12345` |
| Customer | `testuser` | `Test@12345` |

**Change these passwords before any real/public deployment.**

---

## 7. Deployment Notes

### PythonAnywhere
1. Upload the project (or `git clone` it) into your PythonAnywhere account.
2. Create a virtualenv and `pip install -r requirements.txt`.
3. Create a MySQL database from the **Databases** tab (PythonAnywhere provides
   free MySQL for all accounts) and set the `DB_*` env vars to match the host they
   give you (usually `yourusername.mysql.pythonanywhere-services.com`).
4. Set `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`.
5. Configure the **Web** tab to point to `ecommerce_project/wsgi.py`, run
   `python manage.py migrate` and `python manage.py collectstatic` from a Bash console,
   and reload the web app.

### Heroku
1. Add a `Procfile`: `web: gunicorn ecommerce_project.wsgi`
2. Provision the **JawsDB MySQL** or **ClearDB MySQL** add-on and set the `DB_*`
   variables from the add-on's connection string.
3. `heroku config:set DJANGO_DEBUG=False DJANGO_SECRET_KEY=... DJANGO_ALLOWED_HOSTS=yourapp.herokuapp.com`
4. `git push heroku main`, then `heroku run python manage.py migrate`.

### AWS EC2
1. Launch an EC2 instance (Ubuntu), install Python, MySQL server (or use RDS MySQL),
   Nginx, and Gunicorn.
2. Clone the project, `pip install -r requirements.txt` in a virtualenv.
3. Set environment variables (e.g. via a systemd service file or `/etc/environment`).
4. Run `python manage.py migrate` and `collectstatic`, then run Gunicorn behind Nginx
   as a reverse proxy (standard Django + Nginx + Gunicorn deployment pattern).
5. Open port 80/443 in the EC2 security group; add an SSL cert (Let's Encrypt/Certbot)
   for HTTPS.

For all three: set `DJANGO_DEBUG=False`, a strong random `DJANGO_SECRET_KEY`, and the
correct `DJANGO_ALLOWED_HOSTS` before going live.

---

## 8. Notes for Your Internship Report / Viva

- **Why PyMySQL instead of mysqlclient?** `mysqlclient` needs MySQL's C development
  headers to compile, which many student laptops don't have set up. `PyMySQL` is a
  pure-Python driver that works everywhere `pip install` works, and is registered as
  a drop-in replacement via `pymysql.install_as_MySQLdb()` in `settings.py` — the
  Django ORM code is identical either way.
- **Cart design**: implemented as a session-based cart (`cart/cart.py`) rather than a
  database model, so guests can shop without an account and the cart survives across
  page loads via Django sessions.
- **Order integrity**: stock is checked and decremented inside a database transaction
  (`orders/views.py::checkout`) so two customers can't oversell the last unit of stock;
  cancelling an order restocks the items.
- **Extensibility**: the REST API (`catalog/api_urls.py`) demonstrates how the same
  models could power a future mobile app or SPA frontend without touching the
  server-rendered storefront.
