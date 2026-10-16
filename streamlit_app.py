import streamlit as st
import requests
import pandas as pd
import datetime
import calendar
from streamlit_option_menu import option_menu

API_BASE_URL = "http://127.0.0.1:5000"

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

# ----------------------------------------------------
# Modern Mid-Light SaaS Theme & Contrast Styling
# ----------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fix header cut-off and white spacing */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1;
    }

    .stApp {
        background: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1240px;
    }
    
    /* Brand logo */
    .brand-logo-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #0284C7;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Hero Badges */
    .hero-badge-light {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        background: #EEF2FF;
        border: 1px solid #C7D2FE;
        border-radius: 9999px;
        color: #4338CA;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 14px;
    }

    .hero-headline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.1rem;
        line-height: 1.18;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -1px;
        margin-bottom: 16px;
    }
    
    .hero-headline-accent {
        color: #2563EB;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #475569;
        line-height: 1.65;
        margin-bottom: 24px;
    }

    /* Cards */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        margin-bottom: 16px;
    }
    
    .benefit-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        height: 100%;
        border-left: 4px solid #2563EB;
    }

    /* Metric Boxes */
    .metric-box-light {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    }
    
    .metric-val-light {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E40AF;
        line-height: 1.1;
        margin-top: 4px;
    }

    .metric-lbl-light {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* =======================================================
       UNIVERSAL BUTTON STYLING (FIX FOR INVISIBLE / DARK BUTTONS)
       ======================================================= */
    button[kind="secondary"],
    .stButton > button:not([kind="primary"]) {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1.5px solid #CBD5E1 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.05) !important;
    }

    button[kind="secondary"]:hover,
    .stButton > button:not([kind="primary"]):hover {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        border-color: #94A3B8 !important;
    }

    button[kind="primary"],
    .stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 3px 8px rgba(37, 99, 235, 0.25) !important;
    }

    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    /* ==============================================
       FIX FOR INVISIBLE / HOVER-ONLY TABS (CRUCIAL)
       ============================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding-bottom: 6px !important;
        background: transparent !important;
    }
    
    /* Default Tab Style - High contrast text always visible */
    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: #1E293B !important;           /* Dark text so it is always 100% visible */
        background-color: #F1F5F9 !important; /* Soft distinct background */
        border: 1px solid #CBD5E1 !important;
        border-bottom: none !important;
        opacity: 1 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
    }
    
    /* Selected Active Tab */
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }

    /* Force tab text elements inside to inherit high contrast */
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
        font-weight: 700 !important;
    }

    /* Form input styling for clear contrast */
    input, textarea, select {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

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
# SCENARIO 1: PUBLIC LANDING PAGE (Value for Dairy Owners)
# ====================================================
if not st.session_state["authenticated"]:

    # Top Navbar with proper padding
    nav_col1, nav_col2 = st.columns([7, 3])
    with nav_col1:
        st.markdown('<div class="brand-logo-text">🥛 My Dairy App</div>', unsafe_allow_html=True)
    with nav_col2:
        btn_colA, btn_colB = st.columns([1, 1])
        with btn_colA:
            if st.session_state["landing_view"] == "login":
                if st.button("← Back to Home", use_container_width=True):
                    st.session_state["landing_view"] = "home"
                    st.rerun()
        with btn_colB:
            if st.session_state["landing_view"] == "home":
                if st.button("🔐 Admin Login", type="primary", use_container_width=True):
                    st.session_state["landing_view"] = "login"
                    st.rerun()

    st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

    # VIEW A: ADMIN LOGIN FORM
    if st.session_state["landing_view"] == "login":
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown('<div style="text-align:center; padding: 20px 0;">', unsafe_allow_html=True)
            st.markdown('<div class="hero-badge-light">🔒 Administrator Portal</div>', unsafe_allow_html=True)
            st.markdown('<h2 style="color:#0F172A; font-weight:800; margin-bottom:8px;">Sign in to My Dairy App</h2>', unsafe_allow_html=True)
            st.markdown('<p style="color:#64748B;">Enter your administrator credentials to access the central operations panel.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            with st.form("admin_login_form"):
                username = st.text_input("Username", value="admin")
                password = st.text_input("Password", type="password", value="admin@123")
                submit = st.form_submit_button("Sign In to Portal →", type="primary", use_container_width=True)

                if submit:
                    if not username or not password:
                        st.warning("Please provide username and password.")
                    else:
                        try:
                            resp = requests.post(
                                f"{API_BASE_URL}/auth/login",
                                json={"username": username, "password": password},
                                timeout=5
                            )
                            if resp.status_code == 200:
                                data = resp.json()
                                st.session_state["authenticated"] = True
                                st.session_state["username"] = data["user"]["username"]
                                st.session_state["access_token"] = data["access_token"]
                                st.session_state["user_info"] = data["user"]
                                st.success("Login verified! Redirecting to dashboard...")
                                st.rerun()
                            else:
                                err = resp.json().get("message", "Invalid username or password")
                                st.error(f"Login Failed: {err}")
                        except Exception as e:
                            st.error(f"Cannot reach Dairy Backend API: {e}")

    # VIEW B: VALUE-PROPOSITION LANDING PAGE (Why Dairy Owners Need This)
    else:
        # Hero Section
        h_col1, h_col2 = st.columns([6.5, 3.5])
        with h_col1:
            st.markdown('<div class="hero-badge-light">🥛 Built Specifically For Dairy Businesses</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="hero-headline">'
                'Stop Ledger Losses. Digitally Automate Your '
                '<span class="hero-headline-accent">Dairy & Milk Billing</span>'
                '</div>', 
                unsafe_allow_html=True
            )
            st.markdown(
                '<p class="hero-subtitle">'
                'Traditional paper records cause calculation errors, missed morning/evening entries, and delayed customer payments. '
                'My Dairy App automates daily milk delivery logging, monthly billing calculation, and payment dues in real-time.'
                '</p>',
                unsafe_allow_html=True
            )
            
            cta1, cta2 = st.columns([1.1, 1.3])
            with cta1:
                if st.button("Access Admin Dashboard 🚀", type="primary", use_container_width=True):
                    st.session_state["landing_view"] = "login"
                    st.rerun()
            with cta2:
                st.markdown("<p style='color:#64748B; font-size:0.9rem; margin-top:8px;'>✓ 100% Accurate Billing &nbsp; ✓ Zero Missing Entries</p>", unsafe_allow_html=True)
                
        with h_col2:
            st.markdown("""
            <div class="saas-card" style="border: 2px solid #DBEAFE; background:#FFFFFF;">
                <h4 style="color:#1E3A8A; font-weight:800; margin-bottom:12px;">📊 Why Dairy Owners Switch:</h4>
                <div style="margin-bottom:12px;">
                    <strong style="color:#DC2626;">❌ Old Way (Paper Record):</strong>
                    <div style="font-size:0.88rem; color:#64748B;">Disputes with customers over delivery quantities and rates. Delayed month-end bill preparation taking multiple days.</div>
                </div>
                <hr style="border:none; border-top:1px solid #E2E8F0; margin:10px 0;">
                <div>
                    <strong style="color:#16A34A;">✅ New Way (My Dairy App):</strong>
                    <div style="font-size:0.88rem; color:#475569;">1-Click morning/evening milk entry, automatic previous dues carry-forward, and itemized customer invoice ready in seconds.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 4 Key Problems My Dairy App Solves For Your Business")
        st.markdown("<p style='color:#64748B; margin-top:-8px; margin-bottom:20px;'>Manage your whole dairy operation smoothly from a single mobile or laptop screen.</p>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            st.markdown("""
            <div class="benefit-card">
                <h4 style="color:#0F172A; font-weight:700;">1. Shift-Wise Milk Logging (Morning & Evening)</h4>
                <p style="color:#64748B; font-size:0.92rem; line-height:1.5;">Customers often take different quantities in morning vs evening (e.g. 1.5L morning, 0.5L evening). Log entries shift-wise by customer name and product type (Cow Milk, Buffalo Milk) with automatic rate multiplier.</p>
            </div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown("""
            <div class="benefit-card">
                <h4 style="color:#0F172A; font-weight:700;">2. Accurate Customer Passbook & Balance</h4>
                <p style="color:#64748B; font-size:0.92rem; line-height:1.5;">Every customer gets an opening balance ledger. Whenever they make partial or advance payments (via Cash/UPI), balance is adjusted immediately with exact payment date tracking.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        b3, b4 = st.columns(2)
        with b3:
            st.markdown("""
            <div class="benefit-card">
                <h4 style="color:#0F172A; font-weight:700;">3. Instant 1-Click Monthly Invoices</h4>
                <p style="color:#64748B; font-size:0.92rem; line-height:1.5;">No manual sum calculator needed at the end of the month! System aggregates all 30 days of morning/evening milk entries, adds previous pending dues, deducts received payments, and produces clear net payable amount.</p>
            </div>
            """, unsafe_allow_html=True)
        with b4:
            st.markdown("""
            <div class="benefit-card">
                <h4 style="color:#0F172A; font-weight:700;">4. Transparency That Builds Customer Trust</h4>
                <p style="color:#64748B; font-size:0.92rem; line-height:1.5;">Print or share itemized monthly statements showing daily milk quantities and rates. No arguments, complete clarity, and faster payment collections for the dairy owner.</p>
            </div>
            """, unsafe_allow_html=True)

    st.stop()


# ====================================================
# SCENARIO 2: AUTHENTICATED ADMIN USER -> FULL DASHBOARD
# ====================================================

# Top Header Bar with Profile & Navigation
nav_row1, nav_row2 = st.columns([7, 3])
with nav_row1:
    st.markdown('<div class="brand-logo-text">🥛 My Dairy App Control Center</div>', unsafe_allow_html=True)
with nav_row2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    role_badge = st.session_state.get("user_info", {}).get("role", "admin").upper()
    if st.button(f"👤 {st.session_state['username']} [{role_badge}] (Logout)", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.session_state["access_token"] = ""
        st.session_state["user_info"] = {}
        st.session_state["landing_view"] = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Main Navigation Menu (Clean & Modern Mid-Light)
selected_menu = option_menu(
    menu_title=None,
    options=["Dashboard", "Customers", "Products", "Milk Entries", "Payments", "Billing"],
    icons=["speedometer2", "people-fill", "box-seam-fill", "droplet-fill", "credit-card-fill", "receipt-cutoff"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px 12px", 
            "background": "#FFFFFF", 
            "border": "1px solid #CBD5E1",
            "border-radius": "14px", 
            "box-shadow": "0 2px 8px rgba(15, 23, 42, 0.05)",
            "margin-bottom": "24px"
        },
        "icon": {"font-size": "16px"},
        "nav-link": {
            "font-size": "15px", 
            "font-weight": "700", 
            "padding": "10px 16px", 
            "margin": "0px 4px", 
            "border-radius": "10px", 
            "color": "#334155"
        },
        "nav-link-selected": {
            "background": "#2563EB", 
            "color": "#FFFFFF", 
            "box-shadow": "0 4px 12px rgba(37, 99, 235, 0.25)"
        },
    }
)

# ----------------------------------------------------
# 1. ADMIN DASHBOARD
# ----------------------------------------------------
if selected_menu == "Dashboard":
    st.markdown('<div class="hero-badge-light">⚡ Live Operations Overview</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-weight:800; color:#0F172A; margin-bottom:4px;">Operations Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom:24px;">Real-time key business indicators and activity streams.</p>', unsafe_allow_html=True)

    cust_data = api_get("/customers")
    prod_data = api_get("/products")
    milk_data = api_get("/milk-entries")
    payments_data = api_get("/payments")

    c_list = cust_data.get("customers", []) if cust_data else []
    p_list = prod_data.get("products", []) if prod_data else []
    m_list = milk_data.get("milk_entries", []) if milk_data else []
    pay_list = payments_data.get("payment_entries", []) if payments_data else []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-box-light">
            <div class="metric-lbl-light">Active Customers</div>
            <div class="metric-val-light">{len(c_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-box-light">
            <div class="metric-lbl-light">Catalog Products</div>
            <div class="metric-val-light">{len(p_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-box-light">
            <div class="metric-lbl-light">Milk Entries Logged</div>
            <div class="metric-val-light">{len(m_list)}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-box-light">
            <div class="metric-lbl-light">Payments Received</div>
            <div class="metric-val-light">{len(pay_list)}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Live Activity Overview")
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
            st.dataframe(pd.DataFrame(data["customers"]), width='stretch')
        else:
            st.info("No active customer records found.")

    with tab2:
        st.subheader("New Customer Registration")
        with st.form("add_customer"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name")
            mobile = c2.text_input("Mobile Number")
            address = st.text_area("Delivery Address")
            balance = st.number_input("Opening Balance (₹)", min_value=0.0, step=10.0)

            submit = st.form_submit_button("Save Customer", type="primary")
            if submit:
                if not name or not mobile:
                    st.warning("Customer Name and Mobile Number are required.")
                else:
                    res = api_post("/customers", {"name": name, "mobile": mobile, "address": address, "opening_balance": balance})
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
        with st.form("add_product"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Product Name (e.g. Cow Milk, Buffalo Milk, Ghee)")
            unit = c2.selectbox("Unit of Measure", ["Liter", "Kg", "Packet"])
            rate = st.number_input("Rate per Unit (₹)", min_value=0.0, step=1.0)

            submit = st.form_submit_button("Save Product", type="primary")
            if submit:
                if not name:
                    st.warning("Product name is required.")
                else:
                    res = api_post("/products", {"name": name, "unit": unit, "rate": rate})
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
                            st.success("Milk supply entry recorded!")
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
