# 🥛 My Dairy App — Intelligent Dairy Automation Platform

A modern, full-stack Dairy Management & Billing Automation System built with **Flask REST API (Backend)** and **Streamlit (Frontend)**. It automates daily milk delivery tracking (morning & evening shifts), customer passbook ledgers, cash/online payment reconciliation, and 1-click monthly billing invoices with automated dues carry-forward.

---

## 📁 Project Architecture & Directory Structure

```text
Dairy_Management_API/
├── backend/                      # Flask REST API Backend
│   ├── models/                   # SQLAlchemy Database Models
│   │   ├── billing.py            # Monthly bills & ledger calculations
│   │   ├── customers.py          # Customer accounts & opening balances
│   │   ├── milk_entry.py         # Shift milk entries (Morning / Evening)
│   │   ├── payments.py           # Customer payment receipts (Cash / UPI)
│   │   ├── products.py           # Catalog products (Units & Rates)
│   │   └── users.py              # User credentials with salted password hashing
│   ├── routes/                   # API Blueprint Endpoints
│   │   ├── auth_routes.py        # JWT Login, Register, Me endpoints
│   │   ├── customer_routes.py    # Customer CRUD
│   │   ├── products_routes.py    # Product catalog CRUD
│   │   ├── milk_entry_routes.py  # Daily shift delivery logging
│   │   ├── payment_routes.py     # Payment receipts & history
│   │   └── billing_routes.py     # Bill generation & detailed statements
│   ├── app.py                    # Main Flask application entrypoint
│   ├── config.py                 # MySQL & JWT configuration
│   ├── extensions.py             # SQLAlchemy & JWTManager instances
│   ├── seed_admin.py             # Admin seeder & password update utility
│   └── __init__.py
│
├── frontend/                     # Modern Streamlit Web Application
│   ├── .streamlit/
│   │   └── config.toml           # Streamlit theme configuration
│   ├── app.py                    # Streamlit user interface & navigation
│   ├── styles.py                 # Dual Theme Engine (Light Mode ☀️ + Dark Mode 🌙)
│   └── __init__.py
│
├── .env                          # Local environment secrets (not committed to VCS)
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Dependencies & package metadata
└── uv.lock                       # Deterministic dependency lockfile
```

---

## 🛠️ Complete Developer Setup Guide (Start to End)

Follow these steps to set up, configure, and run the project from scratch on any new machine.

### Prerequisites
Before starting, ensure you have the following installed:
1. **Python 3.10+** (Python 3.14 recommended as specified in `pyproject.toml`)
2. **`uv` Package Manager** (High-performance Python package & project manager):
   ```bash
   pip install uv
   ```
3. **MySQL Server** (Running locally via MySQL Community Server, XAMPP, or Docker).

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/Harsh21-design/dairy_management_api.git
cd dairy_management_api
```

---

### Step 2: Configure Environment Variables (`.env`)
Create a `.env` file in the root directory (or update existing) with your local database credentials and JWT security key:

```env
# Database Credentials
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=dairy_management

# Security Configuration
JWT_SECRET_KEY=your_super_secret_jwt_key_here
JWT_ACCESS_TOKEN_EXPIRES=86400
```

> **MySQL Database Setup:**
> Open your MySQL client and create the database if it doesn't already exist:
> ```sql
> CREATE DATABASE IF NOT EXISTS dairy_management;
> ```

---

### Step 3: Install Dependencies
Sync and install all required virtual environment dependencies with `uv`:
```bash
uv sync
```

---

### Step 4: Seed Initial Administrator Account
Run the database seeder script to create all database tables and seed the initial administrator user:
```bash
uv run python backend/seed_admin.py
```
*Note: To specify a custom password during seeding, you can set `ADMIN_DEFAULT_PASSWORD` in your `.env` file, or update it directly via the script.*

---

### Step 5: Start the Development Servers

Because this is a full-stack application, run the backend and frontend in **two separate terminal windows**:

#### **Terminal 1: Start Backend API (Flask)**
```bash
uv run python backend/app.py
```
- Server starts at: **`http://127.0.0.1:5000`**
- Health check: Open `http://127.0.0.1:5000/` to confirm API is online.

#### **Terminal 2: Start Frontend Web App (Streamlit)**
```bash
uv run streamlit run frontend/app.py
```
- Web Application opens at: **`http://localhost:8501`**
- Click **Admin Login**, enter your administrator credentials, and access the Control Center.

---

## 🌟 Key Application Features

1. **Dual Theme Engine (Light ☀️ + Dark 🌙)**:
   - 1-Click theme toggle available on both the Public Landing Page and Admin Dashboard.
   - High-contrast, clean layout for cards, tabs, form inputs, and data tables in both modes.

2. **JWT Security & Password Hashing**:
   - Stateless 256-bit token authorization on protected endpoints.
   - Industry-standard salted password hashes using `werkzeug.security`.

3. **Core Dairy Business Modules**:
   - **👥 Customer Directory & Ledger:** Manage customer contact records, addresses, and initial balance ledgers.
   - **🧀 Product Catalog:** Configure products with custom rates and measurement units (Liter, Kg, Packet).
   - **📝 Shift-Wise Milk Logging:** Record morning and evening milk deliveries with automated rate calculations.
   - **💳 Payment Receipts:** Record cash and digital UPI payments with real-time customer passbook adjustments.
   - **🧾 Automated Billing & Invoicing:** 1-Click monthly statements including previous dues, monthly milk consumption, payments received, and net current balance.

---

## 📡 Core API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/login` | Authenticate user and receive JWT access token |
| `POST` | `/auth/register` | Register a new user/operator account |
| `GET` | `/auth/me` | Fetch authenticated user profile & claims |
| `GET` | `/customers` | Retrieve all active customers |
| `POST` | `/customers` | Register a new customer |
| `GET` | `/products` | List all available dairy products |
| `POST` | `/products` | Add a new dairy product with rate |
| `GET` | `/milk-entries` | Fetch daily milk delivery entries |
| `POST` | `/milk-entries` | Record shift milk entry (Morning / Evening) |
| `GET` | `/payments` | Retrieve customer payment history |
| `POST` | `/payments` | Record customer payment receipt |
| `POST` | `/bills/generate` | Generate monthly consolidated bill for customer |
| `GET` | `/bills/report` | Fetch comprehensive invoice statement with previous dues |
