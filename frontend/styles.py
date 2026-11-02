"""
Theme and CSS Styling Engine for My Dairy App
Supports dynamic Light and Dark mode with high contrast and modern SaaS aesthetics.
"""

def get_theme_css(theme: str = "light") -> str:
    is_dark = (theme == "dark")

    # Theme tokens
    bg_app = "#0B0F19" if is_dark else "#F8FAFC"
    bg_surface = "#111827" if is_dark else "#FFFFFF"
    bg_surface_alt = "#1F2937" if is_dark else "#F1F5F9"
    border_color = "#1F2937" if is_dark else "#E2E8F0"
    border_subtle = "#374151" if is_dark else "#CBD5E1"
    
    text_primary = "#F9FAFB" if is_dark else "#0F172A"
    text_secondary = "#9CA3AF" if is_dark else "#475569"
    text_muted = "#6B7280" if is_dark else "#64748B"
    
    primary_color = "#3B82F6" if is_dark else "#2563EB"
    primary_hover = "#2563EB" if is_dark else "#1D4ED8"
    primary_glow = "rgba(59, 130, 246, 0.25)" if is_dark else "rgba(37, 99, 235, 0.15)"
    
    tab_bg = "#1F2937" if is_dark else "#F1F5F9"
    tab_text = "#D1D5DB" if is_dark else "#1E293B"
    tab_hover_bg = "#374151" if is_dark else "#E2E8F0"
    
    metric_bg = "linear-gradient(135deg, rgba(31, 41, 55, 0.7) 0%, rgba(17, 24, 39, 0.9) 100%)" if is_dark else "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"
    badge_bg = "rgba(59, 130, 246, 0.15)" if is_dark else "#EEF2FF"
    badge_border = "rgba(59, 130, 246, 0.3)" if is_dark else "#C7D2FE"
    badge_text = "#60A5FA" if is_dark else "#4338CA"

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        z-index: 10;
    }}

    .stApp {{
        background: {bg_app} !important;
        color: {text_primary} !important;
    }}

    .block-container {{
        padding-top: 3.2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1240px;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}

    p, span, label {{
        color: {text_secondary};
    }}

    /* Brand Logo */
    .brand-logo-text {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: {primary_color};
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Badges */
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: {badge_bg};
        border: 1px solid {badge_border};
        border-radius: 9999px;
        color: {badge_text};
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 14px;
    }}

    .hero-headline {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        line-height: 1.15;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -1px;
        margin-bottom: 16px;
    }}

    .hero-headline-accent {{
        color: {primary_color};
    }}

    .hero-subtitle {{
        font-size: 1.1rem;
        color: {text_secondary};
        line-height: 1.65;
        margin-bottom: 24px;
    }}

    /* Cards */
    .saas-card {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, {"0.3" if is_dark else "0.04"});
        transition: all 0.25s ease;
        margin-bottom: 16px;
        height: 100%;
    }}

    .saas-card:hover {{
        transform: translateY(-3px);
        border-color: {primary_color};
        box-shadow: 0 12px 28px {primary_glow};
    }}

    .benefit-card {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-left: 4px solid {primary_color};
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, {"0.2" if is_dark else "0.03"});
        height: 100%;
    }}

    .metric-box {{
        background: {metric_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, {"0.25" if is_dark else "0.03"});
        transition: transform 0.2s ease;
    }}

    .metric-box:hover {{
        transform: translateY(-2px);
        border-color: {primary_color};
    }}

    .metric-val {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {primary_color};
        line-height: 1.1;
        margin-top: 4px;
    }}

    .metric-lbl {{
        font-size: 0.8rem;
        color: {text_muted};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    /* Modern Login Container */
    .login-container {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 24px;
        padding: 36px 32px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, {"0.5" if is_dark else "0.08"});
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        height: 42px !important;
    }}

    button[kind="secondary"],
    .stButton > button:not([kind="primary"]) {{
        background-color: {bg_surface} !important;
        color: {text_primary} !important;
        border: 1.5px solid {border_subtle} !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, {"0.2" if is_dark else "0.04"}) !important;
    }}

    button[kind="secondary"]:hover,
    .stButton > button:not([kind="primary"]):hover {{
        background-color: {bg_surface_alt} !important;
        color: {text_primary} !important;
        border-color: {primary_color} !important;
    }}

    button[kind="primary"],
    .stButton > button[kind="primary"] {{
        background-color: {primary_color} !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 12px {primary_glow} !important;
    }}

    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover {{
        background-color: {primary_hover} !important;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px !important;
        border-bottom: 2px solid {border_color} !important;
        padding-bottom: 6px !important;
        background: transparent !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 44px !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: {tab_text} !important;
        background-color: {tab_bg} !important;
        border: 1px solid {border_subtle} !important;
        border-bottom: none !important;
        opacity: 1 !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {tab_hover_bg} !important;
        color: {text_primary} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {primary_color} !important;
        color: #FFFFFF !important;
        border-color: {primary_color} !important;
    }}

    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {{
        color: inherit !important;
        font-weight: 700 !important;
    }}

    /* Form Inputs */
    input, textarea, select {{
        color: {text_primary} !important;
        background-color: {bg_surface} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 8px !important;
    }}

    input:focus, textarea:focus, select:focus {{
        border-color: {primary_color} !important;
        box-shadow: 0 0 0 1px {primary_color} !important;
    }}

    /* Quick Action Pill */
    .action-pill {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, {"0.2" if is_dark else "0.03"});
    }}

    .action-pill:hover {{
        border-color: {primary_color};
        transform: translateY(-2px);
    }}

    /* Hide standard Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
"""

