# 🥛 My Dairy App — Intelligent Dairy Automation Platform

A modern, production-ready full-stack Dairy Management System built with **Flask REST API (Backend)** and **Streamlit (Frontend)**. It automates daily milk delivery tracking (morning & evening), customer passbook ledgers, cash/online payment reconciliation, and 1-click monthly billing invoices with automated dues carry-forward.

---

## 📁 Project Architecture & Directory Structure

```text
Dairy_Management_API/
├── backend/                      # Flask REST API Backend
│   ├── models/                   # SQLAlchemy Database Models
│   │   ├── billing.py            # Monthly bills schema
│   │   ├── customers.py          # Customer ledger & balances
│   │   ├── milk_entry.py         # Shift milk entries (Morning/Evening)
│   │   ├── payments.py           # Payment receipts
│   │   ├── products.py           # Catalog products (Rates & Units)
│   │   └── users.py              # Admin & user credentials with password hashing
│   ├── routes/                   # API Blueprint Endpoints
│   │   ├── auth_routes.py        # JWT Login, Register, User info
│   │   ├── customer_routes.py    # Customer CRUD operations
│   │   ├── products_routes.py    # Product catalog CRUD
│   │   ├── milk_entry_routes.py  # Daily shift delivery operations
│   │   ├── payment_routes.py     # Customer payment receipts
│   │   └── billing_routes.py     # Bill generation & ledger statements
│   ├── app.py                    # Main Flask entrypoint
│   ├── config.py                 # Database & JWT configurations
│   ├── extensions.py             # SQLAlchemy & JWT Manager instances
│   ├── seed_admin.py             # Admin seeder script (admin / admin@123)
│   └── __init__.py
│
├── frontend/                     # Modern Streamlit Web Application
│   ├── .streamlit/
│   │   └── config.toml           # Streamlit theme configuration
│   ├── app.py                    # Streamlit user interface
│   ├── styles.py                 # Theme engine (Light Mode ☀️ + Dark Mode 🌙)
│   └── __init__.py
│
├── .env                          # Database credentials & JWT secret
├── pyproject.toml                # Project dependencies & package metadata
└── uv.lock                       # Deterministic lockfile
```

---

## ⚡ Quick Start Guide

### 1. Initialize Virtual Environment & Dependencies
```bash
uv sync
```

### 2. Seed Default Administrator (One-time setup)
```bash
uv run python backend/seed_admin.py
```
> **Default Admin Credentials:**
> - **Username:** `admin`
> - **Password:** `admin@123`

### 3. Run Backend API Server (Terminal 1)
```bash
uv run python backend/app.py
```
*Flask API runs at `http://127.0.0.1:5000`*

### 4. Run Frontend Streamlit Application (Terminal 2)
```bash
uv run streamlit run frontend/app.py
```
*Web App opens at `http://localhost:8501`*

---

## 🌟 Key Features

1. **Dual Theme Engine (Light ☀️ + Dark 🌙)**:
   - Dynamic real-time toggle available on all screens.
   - High-contrast, crystal-clear readability for cards, tabs, inputs, and tables in both modes.

2. **Secure JWT Authentication**:
   - Backend authenticated via `flask-jwt-extended` with salted password hashing (`werkzeug.security`).
   - Role-based authorization (`admin`, `operator`).

3. **Core Dairy Business Modules**:
   - **👥 Customer Directory & Ledger:** Contact info, delivery address, and live opening balances.
   - **🧀 Product Catalog:** Rates and units (Liter, Kg, Packet) for Cow Milk, Buffalo Milk, Ghee, etc.
   - **📝 Shift-Wise Milk Logging:** Record morning and evening liters separately with automatic rate calculation.
   - **💳 Payment Receipts:** Track customer payments by date with instant passbook balance adjustment.
   - **🧾 Automated Billing & Invoicing:** 1-Click monthly statements including previous dues, monthly milk consumption, payments received, and net current dues.
