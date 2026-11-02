import os
import sys
import streamlit as st
import requests
import pandas as pd
import datetime
import calendar
from streamlit_option_menu import option_menu

# Ensure frontend directory is in sys.path
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from styles import get_theme_css

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")

st.set_page_config(
    page_title="My Dairy App — Modern Dairy Automation Platform",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "access_token" not in st.session_state:
    st.session_state["access_token"] = ""
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {}
if "landing_view" not in st.session_state:
    st.session_state["landing_view"] = "home"  # 'home' or 'login'
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"  # 'light' or 'dark'
if "active_nav_index" not in st.session_state:
    st.session_state["active_nav_index"] = 0

# ----------------------------------------------------
# Apply Active Theme CSS (Light or Dark)
# ----------------------------------------------------
st.markdown(get_theme_css(st.session_state["theme"]), unsafe_allow_html=True)

# ----------------------------------------------------
# API Helper Functions
# ----------------------------------------------------
def get_auth_headers():
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def api_get(endpoint, params=None):
    try:
        headers = get_auth_headers()
        res = requests.get(f"{API_BASE_URL}{endpoint}", params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def api_post(endpoint, json_data):
    try:
        headers = get_auth_headers()
        return requests.post(f"{API_BASE_URL}{endpoint}", json=json_data, headers=headers, timeout=5)
    except Exception:
        return None

# ====================================================
# SCENARIO 1: PUBLIC LANDING & AUTHENTICATION
# ====================================================
if not st.session_state["authenticated"]:

    # Top Navbar with Theme Switcher and Login Actions
    nav_col1, nav_col2 = st.columns([6.5, 3.5])
    with nav_col1:
        st.markdown('<div class="brand-logo-text">🥛 My Dairy App</div>', unsafe_allow_html=True)
    with nav_col2:
        btn_theme_col, btn_action_col = st.columns([1, 1.3])
        with btn_theme_col:
            # Theme Toggle Button
            if st.session_state["theme"] == "light":
                if st.button("🌙 Dark", key="theme_toggle_public", use_container_width=True):
                    st.session_state["theme"] = "dark"
                    st.rerun()
            else:
                if st.button("☀️ Light", key="theme_toggle_public", use_container_width=True):
                    st.session_state["theme"] = "light"
                    st.rerun()

        with btn_action_col:
            if st.session_state["landing_view"] == "login":
                if st.button("← Back to Home", key="btn_back_home", use_container_width=True):
                    st.session_state["landing_view"] = "home"
                    st.rerun()
            else:
                if st.button("🔐 Admin Login", key="btn_admin_login", type="primary", use_container_width=True):
                    st.session_state["landing_view"] = "login"
                    st.rerun()

    st.markdown("<hr style='border:none; border-top:1px solid rgba(148, 163, 184, 0.25); margin: 15px 0 28px 0;'>", unsafe_allow_html=True)

    # ------------------------------------------------
    # VIEW A: MODERNIZED LOGIN PAGE
    # ------------------------------------------------
    if st.session_state["landing_view"] == "login":
        col_l1, col_l2, col_l3 = st.columns([1, 1.8, 1])
        with col_l2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 24px;">
                <div class="hero-badge">🔒 Secure Administrator Portal</div>
                <h2 style="font-weight: 800; margin-bottom: 8px;">Sign in to My Dairy App</h2>
                <p style="font-size: 0.95rem;">Enter your verified credentials to access operations, customer ledgers, and billing.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="login-container">', unsafe_allow_html=True)
                
                with st.form("admin_login_form"):
                    username = st.text_input("Username", value="admin", placeholder="Enter username")
                    password = st.text_input("Password", type="password", value="admin@123", placeholder="Enter password")
                    
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    submit = st.form_submit_button("Sign In to Control Center →", type="primary", use_container_width=True)

                    if submit:
                        if not username or not password:
                            st.warning("Please provide username and password.")
                        else:
                            try:
                                resp = requests.post(
                                    f"{API_BASE_URL}/auth/login",
                                    json={"username": username.strip(), "password": password.strip()},
                                    timeout=5
                                )
                                if resp.status_code == 200:
                                    data = resp.json()
                                    st.session_state["authenticated"] = True
                                    st.session_state["username"] = data["user"]["username"]
                                    st.session_state["access_token"] = data["access_token"]
                                    st.session_state["user_info"] = data["user"]
                                    st.success("Authentication successful! Loading dashboard...")
                                    st.rerun()
                                else:
                                    err = resp.json().get("message", "Invalid username or password")
                                    st.error(f"Authentication Failed: {err}")
                            except Exception as e:
                                st.error(f"Cannot connect to Dairy Backend API: {e}")

                st.markdown("<hr style='border:none; border-top:1px solid rgba(148, 163, 184, 0.2); margin: 18px 0;'>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='text-align:center; font-size:0.85rem; color: #64748B;'>"
                    "Default Credentials: <strong>admin</strong> / <strong>admin@123</strong><br>"
                    "🔐 Secured with JWT 256-bit token verification"
                    "</div>",
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------
    # VIEW B: MODERN VALUE-PROPOSITION LANDING PAGE
    # ------------------------------------------------
    else:
        h_col1, h_col2 = st.columns([6.3, 3.7])
        with h_col1:
            st.markdown('<div class="hero-badge">🥛 Built Specifically For Dairy Businesses</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="hero-headline">'
                'Stop Ledger Losses. Digitally Automate Your '
                '<span class="hero-headline-accent">Dairy & Milk Billing</span>'
                '</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<p class="hero-subtitle">'
                'Traditional paper records cause calculation mistakes, missed morning/evening delivery shifts, and delayed customer payments. '
                'My Dairy App automates daily milk supply tracking, customer passbooks, and monthly billing calculations in real-time.'
                '</p>',
                unsafe_allow_html=True
            )

            cta1, cta2 = st.columns([1.2, 1.4])
            with cta1:
                if st.button("Launch Admin Portal 🚀", type="primary", use_container_width=True):
                    st.session_state["landing_view"] = "login"
                    st.rerun()
            with cta2:
                st.markdown("<p style='font-size:0.9rem; margin-top:10px;'>✓ 100% Accurate Invoicing &nbsp; ✓ Dual Light / Dark Theme</p>", unsafe_allow_html=True)

        with h_col2:
            st.markdown(f"""
            <div class="saas-card" style="border: 2px solid {'#3B82F6' if st.session_state['theme'] == 'dark' else '#DBEAFE'};">
                <h4 style="font-weight: 800; margin-bottom: 14px;">📊 Why Dairy Owners Switch:</h4>
                <div style="margin-bottom: 14px;">
                    <strong style="color: #EF4444;">❌ Traditional Paper Records:</strong>
                    <div style="font-size: 0.9rem; margin-top: 4px;">Frequent disputes over missing milk quantities and rates. Month-end manual calculations taking 2-3 days with high risk of human error.</div>
                </div>
                <hr style="border:none; border-top: 1px solid rgba(148, 163, 184, 0.25); margin: 12px 0;">
                <div>
                    <strong style="color: #10B981;">✅ Automated My Dairy App:</strong>
                    <div style="font-size: 0.9rem; margin-top: 4px;">1-Click morning/evening milk entry, automatic previous dues carry-forward, and itemized customer statements ready in 5 seconds.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 4 Key Problems My Dairy App Solves For Your Business")
        st.markdown("<p style='margin-top:-6px; margin-bottom:22px;'>Manage your whole dairy operation smoothly from a single mobile or desktop screen.</p>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            st.markdown("""
            <div class="benefit-card">
                <h4>1. Shift-Wise Milk Logging (Morning & Evening)</h4>
                <p style="font-size:0.92rem; line-height:1.55;">Customers often take different quantities in morning vs evening (e.g. 1.5L morning, 0.5L evening). Log entries shift-wise by customer name and product type (Cow Milk, Buffalo Milk) with automatic rate multiplier.</p>
            </div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown("""
            <div class="benefit-card">
                <h4>2. Accurate Customer Passbook & Balance</h4>
                <p style="font-size:0.92rem; line-height:1.55;">Every customer gets an opening balance ledger. Whenever they make partial or advance payments (via Cash/UPI), balance is adjusted immediately with exact payment date tracking.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        b3, b4 = st.columns(2)
        with b3:
            st.markdown("""
            <div class="benefit-card">
                <h4>3. Instant 1-Click Monthly Invoices</h4>
                <p style="font-size:0.92rem; line-height:1.55;">No manual sum calculator needed at the end of the month! System aggregates all 30 days of morning/evening milk entries, adds previous pending dues, deducts received payments, and produces clear net payable amount.</p>
            </div>
            """, unsafe_allow_html=True)
        with b4:
            st.markdown("""
            <div class="benefit-card">
                <h4>4. Transparency That Builds Customer Trust</h4>
                <p style="font-size:0.92rem; line-height:1.55;">Print or share itemized monthly statements showing daily milk quantities and rates. No arguments, complete clarity, and faster payment collections for the dairy owner.</p>
            </div>
            """, unsafe_allow_html=True)

    st.stop()


# ====================================================
# SCENARIO 2: AUTHENTICATED ADMIN USER -> FULL DASHBOARD
# ====================================================

# Top Header Bar with Profile, Theme Switcher, and Logout
nav_row1, nav_row2 = st.columns([6.8, 3.2])
with nav_row1:
    st.markdown('<div class="brand-logo-text">🥛 My Dairy App Control Center</div>', unsafe_allow_html=True)
with nav_row2:
    theme_btn_col, logout_btn_col = st.columns([1, 1.7])
    with theme_btn_col:
        # Dynamic Theme Toggle
        if st.session_state["theme"] == "light":
            if st.button("🌙 Dark", key="theme_toggle_admin", use_container_width=True):
                st.session_state["theme"] = "dark"
                st.rerun()
        else:
            if st.button("☀️ Light", key="theme_toggle_admin", use_container_width=True):
                st.session_state["theme"] = "light"
                st.rerun()

    with logout_btn_col:
        role_badge = st.session_state.get("user_info", {}).get("role", "admin").upper()
        if st.button(f"👤 {st.session_state['username']} [{role_badge}] (Logout)", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.session_state["access_token"] = ""
            st.session_state["user_info"] = {}
            st.session_state["landing_view"] = "home"
            st.rerun()

# Dynamic Option Menu Palette based on theme
is_dark = (st.session_state["theme"] == "dark")
menu_bg = "#111827" if is_dark else "#FFFFFF"
menu_border = "#1F2937" if is_dark else "#CBD5E1"
menu_text = "#E5E7EB" if is_dark else "#334155"

selected_menu = option_menu(
    menu_title=None,
    options=["Dashboard", "Customers", "Products", "Milk Entries", "Payments", "Billing"],
    icons=["speedometer2", "people-fill", "box-seam-fill", "droplet-fill", "credit-card-fill", "receipt-cutoff"],
    default_index=st.session_state.get("active_nav_index", 0),
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px 12px",
            "background": menu_bg,
            "border": f"1px solid {menu_border}",
            "border-radius": "14px",
            "box-shadow": "0 4px 14px rgba(0, 0, 0, 0.15)" if is_dark else "0 2px 8px rgba(15, 23, 42, 0.05)",
            "margin-bottom": "24px"
        },
        "icon": {"font-size": "16px"},
        "nav-link": {
            "font-size": "15px",
            "font-weight": "700",
            "padding": "10px 16px",
            "margin": "0px 4px",
            "border-radius": "10px",
            "color": menu_text
        },
        "nav-link-selected": {
            "background": "#3B82F6" if is_dark else "#2563EB",
            "color": "#FFFFFF",
            "box-shadow": "0 4px 12px rgba(37, 99, 235, 0.3)"
        },
    }
)

# ----------------------------------------------------
# 1. ADMIN DASHBOARD
# ----------------------------------------------------
if selected_menu == "Dashboard":
    full_name = st.session_state.get("user_info", {}).get("full_name") or st.session_state.get("username", "Admin")
    st.markdown(f'<div class="hero-badge">⚡ Live Dairy Intelligence</div>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-weight:800; margin-bottom:4px;">Welcome back, {full_name}! 👋</h2>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom:24px;">Real-time overview of dairy deliveries, customer balances, and collections ledger.</p>', unsafe_allow_html=True)

    # Fetch live data
    cust_data = api_get("/customers")
    prod_data = api_get("/products")
    milk_data = api_get("/milk-entries")
    payments_data = api_get("/payments")

    c_list = cust_data.get("customers", []) if cust_data else []
    p_list = prod_data.get("products", []) if prod_data else []
    m_list = milk_data.get("milk_entries", []) if milk_data else []
    pay_list = payments_data.get("payment_entries", []) if payments_data else []

    # KPI Metric Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-lbl">Active Customers</div>
            <div class="metric-val">{len(c_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-lbl">Catalog Products</div>
            <div class="metric-val">{len(p_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-lbl">Milk Entries Logged</div>
            <div class="metric-val">{len(m_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-lbl">Payments Recorded</div>
            <div class="metric-val">{len(pay_list)}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Workflow Shortcuts
    st.subheader("⚡ Quick Operations Control")
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        st.markdown("""
        <div class="saas-card" style="padding:18px;">
            <div style="font-size:1.4rem; margin-bottom:6px;">🥛</div>
            <strong style="display:block; margin-bottom:4px;">Daily Milk Supply</strong>
            <span style="font-size:0.85rem;">Record shift delivery for customers.</span>
        </div>
        """, unsafe_allow_html=True)
    with qa2:
        st.markdown("""
        <div class="saas-card" style="padding:18px;">
            <div style="font-size:1.4rem; margin-bottom:6px;">👥</div>
            <strong style="display:block; margin-bottom:4px;">Customer Passbook</strong>
            <span style="font-size:0.85rem;">Manage balances & contacts.</span>
        </div>
        """, unsafe_allow_html=True)
    with qa3:
        st.markdown("""
        <div class="saas-card" style="padding:18px;">
            <div style="font-size:1.4rem; margin-bottom:6px;">💳</div>
            <strong style="display:block; margin-bottom:4px;">Payment Receipt</strong>
            <span style="font-size:0.85rem;">Log customer cash & UPI receipts.</span>
        </div>
        """, unsafe_allow_html=True)
    with qa4:
        st.markdown("""
        <div class="saas-card" style="padding:18px;">
            <div style="font-size:1.4rem; margin-bottom:6px;">🧾</div>
            <strong style="display:block; margin-bottom:4px;">Monthly Invoicing</strong>
            <span style="font-size:0.85rem;">Generate net balance statements.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Live Activity Stream")
    d_tab1, d_tab2, d_tab3 = st.tabs(["📋 Recent Milk Entries", "👥 Customer Directory", "🧀 Product Catalog"])

    with d_tab1:
        if m_list:
            st.dataframe(pd.DataFrame(m_list).tail(10), width='stretch')
        else:
            st.info("No milk entries recorded yet.")

    with d_tab2:
        if c_list:
            st.dataframe(pd.DataFrame(c_list), width='stretch')
        else:
            st.info("No customers registered yet.")

    with d_tab3:
        if p_list:
            st.dataframe(pd.DataFrame(p_list), width='stretch')
        else:
            st.info("No products cataloged yet.")

# ----------------------------------------------------
# 2. CUSTOMERS MANAGEMENT
# ----------------------------------------------------
elif selected_menu == "Customers":
    st.title("👥 Customer Directory & Ledger")
    tab1, tab2 = st.tabs(["📋 Registered Customers", "➕ Onboard New Customer"])

    with tab1:
        data = api_get("/customers")
        if data and data.get("customers"):
            custs = data["customers"]
            search_query = st.text_input("🔍 Search customer by name or phone:", placeholder="Type name or mobile...")
            if search_query:
                custs = [c for c in custs if search_query.lower() in str(c.get("name", "")).lower() or search_query in str(c.get("mobile", ""))]
            
            if custs:
                st.dataframe(pd.DataFrame(custs), width='stretch')
            else:
                st.warning("No matching customers found.")
        else:
            st.info("No active customer records found.")

    with tab2:
        st.subheader("New Customer Registration")
        with st.form("add_customer"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name", placeholder="Customer Name")
            mobile = c2.text_input("Mobile Number", placeholder="10-digit Phone")
            address = st.text_area("Delivery Address", placeholder="Street, Colony, Landmark")
            balance = st.number_input("Opening Balance (₹)", min_value=0.0, step=10.0, help="Initial pending balance if any")

            submit = st.form_submit_button("Save Customer", type="primary")
            if submit:
                if not name or not mobile:
                    st.warning("Customer Name and Mobile Number are required.")
                else:
                    res = api_post("/customers", {"name": name.strip(), "mobile": mobile.strip(), "address": address.strip(), "opening_balance": balance})
                    if res and res.status_code == 201:
                        st.success(f"Customer '{name}' registered successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to register customer.")

# ----------------------------------------------------
# 3. PRODUCTS MANAGEMENT
# ----------------------------------------------------
elif selected_menu == "Products":
    st.title("🧀 Product Catalog")
    tab1, tab2 = st.tabs(["📋 Available Products", "➕ Add New Product"])

    with tab1:
        data = api_get("/products")
        if data and data.get("products"):
            st.dataframe(pd.DataFrame(data["products"]), width='stretch')
        else:
            st.info("No products found in catalog.")

    with tab2:
        st.subheader("Add New Dairy Product")
        with st.form("add_product"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Product Name", placeholder="e.g. Cow Milk, Buffalo Milk, Ghee")
            unit = c2.selectbox("Unit of Measure", ["Liter", "Kg", "Packet"])
            rate = st.number_input("Rate per Unit (₹)", min_value=0.0, step=1.0)

            submit = st.form_submit_button("Save Product", type="primary")
            if submit:
                if not name:
                    st.warning("Product name is required.")
                else:
                    res = api_post("/products", {"name": name.strip(), "unit": unit, "rate": rate})
                    if res and res.status_code == 201:
                        st.success(f"Product '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add product.")

# ----------------------------------------------------
# 4. MILK ENTRIES MANAGEMENT
# ----------------------------------------------------
elif selected_menu == "Milk Entries":
    st.title("📝 Daily Milk Entry Log")

    cust_data = api_get("/customers")
    prod_data = api_get("/products")

    cust_map = {c["name"]: c["id"] for c in cust_data.get("customers", [])} if cust_data else {}
    prod_map = {p["name"]: p["id"] for p in prod_data.get("products", [])} if prod_data else {}

    tab1, tab2 = st.tabs(["📋 View Daily Entries", "➕ Record Milk Supply"])

    with tab1:
        entries = api_get("/milk-entries")
        if entries and entries.get("milk_entries"):
            st.dataframe(pd.DataFrame(entries["milk_entries"]), width='stretch')
        else:
            st.info("No milk supply entries recorded.")

    with tab2:
        st.subheader("Log Shift Milk Delivery")
        if not cust_map or not prod_map:
            st.warning("Please make sure you have at least 1 Customer and 1 Product registered first.")
        else:
            with st.form("add_milk_entry"):
                c1, c2 = st.columns(2)
                selected_cust = c1.selectbox("Select Customer", list(cust_map.keys()))
                selected_prod = c2.selectbox("Select Product", list(prod_map.keys()))

                entry_date = st.date_input("Supply Date", datetime.date.today())

                q1, q2 = st.columns(2)
                m_qty = q1.number_input("Morning Quantity (Liters)", min_value=0.0, step=0.5)
                e_qty = q2.number_input("Evening Quantity (Liters)", min_value=0.0, step=0.5)

                submit = st.form_submit_button("Save Milk Entry", type="primary")
                if submit:
                    if m_qty == 0 and e_qty == 0:
                        st.warning("Please specify at least Morning or Evening quantity.")
                    else:
                        payload = {
                            "customer_id": cust_map[selected_cust],
                            "product_id": prod_map[selected_prod],
                            "entry_date": entry_date.strftime("%Y-%m-%d"),
                            "morning_qty": m_qty,
                            "evening_qty": e_qty
                        }
                        res = api_post("/milk-entries", payload)
                        if res and res.status_code == 201:
                            st.success("Milk supply entry recorded successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {res.json().get('message') if res else 'API Failed'}")

# ----------------------------------------------------
# 5. PAYMENTS MANAGEMENT
# ----------------------------------------------------
elif selected_menu == "Payments":
    st.title("💳 Payment Receipts & Reconciliation")

    cust_data = api_get("/customers")
    prod_data = api_get("/products")

    cust_map = {c["name"]: c["id"] for c in cust_data.get("customers", [])} if cust_data else {}
    prod_map = {p["name"]: p["id"] for p in prod_data.get("products", [])} if prod_data else {}

    tab1, tab2 = st.tabs(["📋 Payment History", "➕ Record Customer Payment"])

    with tab1:
        st.subheader("All Customer Payment Receipts")
        payments = api_get("/payments")
        if payments and payments.get("payment_entries"):
            df_pay = pd.DataFrame(payments["payment_entries"])
            st.dataframe(df_pay, width='stretch')
        else:
            st.info("No payment records found.")

    with tab2:
        st.subheader("Record New Payment Receipt")
        if not cust_map or not prod_map:
            st.warning("Please add customers and products first.")
        else:
            with st.form("add_payment"):
                c1, c2 = st.columns(2)
                selected_cust = c1.selectbox("Customer Name", list(cust_map.keys()))
                selected_prod = c2.selectbox("Associated Product", list(prod_map.keys()))

                p_date = st.date_input("Payment Received Date", datetime.date.today())
                amount = st.number_input("Amount Received (₹)", min_value=0.0, step=50.0)

                submit = st.form_submit_button("Record Payment", type="primary")
                if submit:
                    if amount <= 0:
                        st.warning("Payment amount must be greater than 0.")
                    else:
                        payload = {
                            "customer_id": cust_map[selected_cust],
                            "product_id": prod_map[selected_prod],
                            "payment_date": p_date.strftime("%Y-%m-%d"),
                            "amount": amount
                        }
                        res = api_post("/payments", payload)
                        if res and res.status_code == 201:
                            st.success("Payment receipt recorded successfully!")
                            st.rerun()
                        else:
                            err_text = res.json().get("message") if res else "API Error"
                            st.error(f"Failed: {err_text}")

# ----------------------------------------------------
# 6. BILLING & INVOICES
# ----------------------------------------------------
elif selected_menu == "Billing":
    st.title("🧾 Billing & Customer Invoices")

    cust_data = api_get("/customers")
    cust_map = {c["name"]: c["id"] for c in cust_data.get("customers", [])} if cust_data else {}

    tab1, tab2 = st.tabs(["⚙️ Generate Monthly Bill", "📄 Detailed Statement & Invoice"])

    with tab1:
        st.subheader("Generate Customer Monthly Bill")
        if not cust_map:
            st.warning("No customers available.")
        else:
            with st.form("gen_bill"):
                c1, c2, c3 = st.columns(3)
                selected_cust = c1.selectbox("Select Customer", list(cust_map.keys()))
                today = datetime.date.today()
                month = c2.number_input("Month (1-12)", min_value=1, max_value=12, value=today.month)
                year = c3.number_input("Year", min_value=2020, max_value=2030, value=today.year)

                submit = st.form_submit_button("Generate Bill", type="primary")
                if submit:
                    payload = {
                        "customer_id": cust_map[selected_cust],
                        "bill_month": month,
                        "bill_year": year
                    }
                    res = api_post("/bills/generate", payload)
                    if res and res.status_code == 201:
                        st.success(f"Bill generated for {calendar.month_name[month]} {year}!")
                        st.rerun()
                    else:
                        st.error(f"Notice: {res.json().get('message') if res else 'Failed to generate'}")

    with tab2:
        st.subheader("View Customer Ledger & Invoice Report")
        if cust_map:
            c1, c2, c3 = st.columns(3)
            rep_cust = c1.selectbox("Customer", list(cust_map.keys()), key="rep_cust")
            today = datetime.date.today()
            rep_month = c2.number_input("Month", min_value=1, max_value=12, value=today.month, key="rep_m")
            rep_year = c3.number_input("Year", min_value=2020, max_value=2030, value=today.year, key="rep_y")

            if st.button("Fetch Invoice Report", type="primary"):
                report = api_get("/bills/report", params={
                    "customer_id": cust_map[rep_cust],
                    "bill_month": rep_month,
                    "bill_year": rep_year
                })
                if report and "summary" in report:
                    st.success("Invoice Statement Retrieved!")
                    summary = report["summary"]

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Previous Due", f"₹{summary['previous_due']}")
                    m2.metric("Current Milk Charges", f"₹{summary['total_amount']}")
                    m3.metric("Total Payments", f"₹{summary['total_payment']}")
                    m4.metric("Net Current Due", f"₹{summary['current_due']}")

                    st.divider()
                    st.subheader("Milk Supplies Detail")
                    if report.get("milk_entries"):
                        st.dataframe(pd.DataFrame(report["milk_entries"]), width='stretch')
                    else:
                        st.info("No milk entries recorded for this period.")

                    st.subheader("Payments Received")
                    if report.get("payments"):
                        st.dataframe(pd.DataFrame(report["payments"]), width='stretch')
                    else:
                        st.info("No payments recorded for this period.")
                else:
                    st.error(report.get("message") if report else "Could not fetch report.")

