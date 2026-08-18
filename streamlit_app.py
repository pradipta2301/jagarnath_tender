import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Tender Intelligence Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM UI / CSS
# ============================================================
st.markdown("""
<style>
/* ---------- Global ---------- */
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.08), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.07), transparent 25%),
        #f5f7fb;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1500px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #172554 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(255,255,255,0.16) !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] .stDateInput input {
    background: rgba(255,255,255,0.09) !important;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 25px 30px 24px;
    border-radius: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0369a1 100%);
    color: white;
    box-shadow: 0 14px 35px rgba(15, 23, 42, 0.18);
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}

.hero-kicker {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #bfdbfe;
    margin-bottom: 5px;
}

.hero-title {
    font-size: 2.25rem;
    line-height: 1.1;
    font-weight: 800;
    margin: 0;
}

.hero-subtitle {
    color: #dbeafe;
    margin: 8px 0 0;
    font-size: 1rem;
}

.hero-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 11px;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 0.78rem;
}

/* ---------- Section headings ---------- */
.section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    margin: 8px 0 12px;
}

/* ---------- KPI cards ---------- */
.kpi-card {
    position: relative;
    background: rgba(255,255,255,0.94);
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 16px 18px;
    min-height: 108px;
    box-shadow: 0 7px 20px rgba(15,23,42,0.06);
    transition: all .2s ease;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 13px 28px rgba(15,23,42,0.11);
}

.kpi-card:after {
    content: "";
    position: absolute;
    right: -28px;
    bottom: -35px;
    width: 95px;
    height: 95px;
    border-radius: 50%;
    background: rgba(59,130,246,0.07);
}

.kpi-icon {
    font-size: 1.2rem;
    margin-bottom: 5px;
}

.kpi-label {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 800;
    letter-spacing: .6px;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 1.75rem;
    line-height: 1.2;
    color: #0f172a;
    font-weight: 800;
    margin-top: 3px;
}

.kpi-blue { border-top: 4px solid #2563eb; }
.kpi-green { border-top: 4px solid #16a34a; }
.kpi-orange { border-top: 4px solid #f59e0b; }
.kpi-purple { border-top: 4px solid #7c3aed; }
.kpi-cyan { border-top: 4px solid #0891b2; }

/* ---------- Chart containers ---------- */
.chart-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 8px 10px 2px;
    box-shadow: 0 7px 20px rgba(15,23,42,0.05);
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    font-weight: 700 !important;
    opacity: 1 !important; /* Keeps tabs visible without needing to hover */
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb !important;
}

/* ---------- Dataframe ---------- */
div[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 7px 20px rgba(15,23,42,0.05);
}

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

/* ---------- Small footer ---------- */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: .75rem;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data(ttl=600)
def load_data():
    file_path = "odisha_tenders.xlsx"

    if not os.path.exists(file_path):
        file_path = "odisha_tenders.xlsx"

    try:
        df = pd.read_excel(file_path)

        if "Tender Value" in df.columns:
            df["Tender Value"] = pd.to_numeric(
                df["Tender Value"], errors="coerce"
            ).fillna(0)

        for date_col in ["Published Date", "Opening Date", "Closing Date"]:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(
                    df[date_col], errors="coerce"
                )

        # Identify source portal
        if "Tender No" in df.columns:
            def identify_source(t_no):
                t_no_str = str(t_no).strip().upper()
                return "GeM" if t_no_str.startswith("GEM") else "NIC / State Portal"

            idx = df.columns.get_loc("Tender No") + 1
            df.insert(
                idx,
                "Source Portal",
                df["Tender No"].apply(identify_source),
            )

        # Normalize links
        def get_valid_link(row):
            link = str(row.get("Link", "")).strip()
            t_no = str(row.get("Tender No", "")).strip()

            if link.startswith("http"):
                return link

            if t_no.upper().startswith("GEM"):
                return f"https://bidplus.gem.gov.in/all-bids?q={t_no}"

            return "https://tenders.odisha.gov.in"

        if "Link" in df.columns:
            df["Link"] = df.apply(get_valid_link, axis=1)
        else:
            df["Link"] = "https://bidplus.gem.gov.in/all-bids"

        return df

    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")
        return pd.DataFrame()


df = load_data()

# ============================================================
# EMPTY STATE
# ============================================================
if df.empty:
    st.warning(
        "No tender data found. Please keep the Excel file in the same "
        "folder as this Streamlit application."
    )
    st.stop()


# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Odisha Government Procurement</div>
    <div class="hero-title">🏛️ Tender Intelligence Dashboard</div>
    <div class="hero-subtitle">
        Search, filter and analyse government tenders from multiple Odisha portals
        in one place.
    </div>
    <div class="hero-badge">● Live dataset • Intelligent filtering • Tender tracking</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.markdown("## 🎯 Tender Filters")
st.sidebar.caption("Narrow down the opportunities you want to track.")

search_query = st.sidebar.text_input(
    "🔎 Search",
    placeholder="Tender title, ID or keyword..."
)

if "Source Portal" in df.columns:
    sources = [
        d for d in df["Source Portal"].dropna().unique().tolist()
        if str(d).strip()
    ]
    selected_sources = st.sidebar.multiselect(
        "🌐 Source Portal",
        options=sorted(sources),
    )
else:
    selected_sources = []

if "District" in df.columns:
    districts = [
        d for d in df["District"].dropna().unique().tolist()
        if str(d).strip()
    ]
    selected_districts = st.sidebar.multiselect(
        "📍 District",
        options=sorted(districts),
    )
else:
    selected_districts = []

if "Department" in df.columns:
    depts = [
        d for d in df["Department"].dropna().unique().tolist()
        if str(d).strip()
    ]
    selected_depts = st.sidebar.multiselect(
        "🏢 Department",
        options=sorted(depts),
    )
else:
    selected_depts = []

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Date Filters")

selected_pub_date = []
min_pub, max_pub = None, None
if "Published Date" in df.columns and not df["Published Date"].dropna().empty:
    min_pub = df["Published Date"].min().date()
    max_pub = df["Published Date"].max().date()

    selected_pub_date = st.sidebar.date_input(
        "Published Date",
        value=(min_pub, max_pub),
        min_value=min_pub,
        max_value=max_pub,
    )

selected_close_date = []
min_close, max_close = None, None
if "Closing Date" in df.columns and not df["Closing Date"].dropna().empty:
    min_close = df["Closing Date"].min().date()
    max_close = df["Closing Date"].max().date()

    selected_close_date = st.sidebar.date_input(
        "Closing Date",
        value=(min_close, max_close),
        min_value=min_close,
        max_value=max_close,
    )

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: combine portal + district + department filters for faster prospecting.")


# ============================================================
# APPLY FILTERS
# ============================================================
filtered_df = df.copy()

if search_query:
    search_mask = (
        filtered_df["Title"].astype(str).str.contains(
            search_query, case=False, na=False
        )
        | filtered_df["Tender No"].astype(str).str.contains(
            search_query, case=False, na=False
        )
    )

    if "Summary" in filtered_df.columns:
        search_mask |= filtered_df["Summary"].astype(str).str.contains(
            search_query, case=False, na=False
        )

    filtered_df = filtered_df[search_mask]

if selected_sources:
    filtered_df = filtered_df[
        filtered_df["Source Portal"].isin(selected_sources)
    ]

if selected_districts:
    filtered_df = filtered_df[
        filtered_df["District"].isin(selected_districts)
    ]

if selected_depts:
    filtered_df = filtered_df[
        filtered_df["Department"].isin(selected_depts)
    ]

# ONLY drop records if the user specifically changes the date from the min/max defaults
if len(selected_pub_date) == 2:
    start_pub, end_pub = selected_pub_date
    if start_pub != min_pub or end_pub != max_pub:
        filtered_df = filtered_df[
            (filtered_df["Published Date"].dt.date >= start_pub)
            & (filtered_df["Published Date"].dt.date <= end_pub)
        ]

# ONLY drop records if the user specifically changes the date from the min/max defaults
if len(selected_close_date) == 2:
    start_close, end_close = selected_close_date
    if start_close != min_close or end_close != max_close:
        filtered_df = filtered_df[
            (filtered_df["Closing Date"].dt.date >= start_close)
            & (filtered_df["Closing Date"].dt.date <= end_close)
        ]


# ============================================================
# KPI CALCULATIONS
# ============================================================
total_tenders = len(filtered_df)
today = datetime.now().date()
active_count = 0

if not filtered_df.empty:
    is_opened = pd.Series(True, index=filtered_df.index)

    if "Opening Date" in filtered_df.columns:
        is_opened = (
            filtered_df["Opening Date"].dt.date <= today
        )

        if "Published Date" in filtered_df.columns:
            is_opened |= (
                filtered_df["Opening Date"].isna()
                & (filtered_df["Published Date"].dt.date <= today)
            )

    if "Closing Date" in filtered_df.columns:
        is_active = is_opened & (
            filtered_df["Closing Date"].isna()
            | (filtered_df["Closing Date"].dt.date >= today)
        )
        active_count = int(is_active.sum())
    else:
        active_count = int(is_opened.sum())

dist_count = (
    filtered_df["District"].nunique()
    if "District" in filtered_df.columns else 0
)

dept_count = (
    filtered_df["Department"].nunique()
    if "Department" in filtered_df.columns else 0
)

portal_count = (
    filtered_df["Source Portal"].nunique()
    if "Source Portal" in filtered_df.columns else 0
)

total_value = (
    filtered_df["Tender Value"].sum()
    if "Tender Value" in filtered_df.columns else 0
)


# ============================================================
# KPI CARDS
# ============================================================
st.markdown('<div class="section-title">📌 Opportunity Snapshot</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

cards = [
    (k1, "kpi-blue", "📋", "Total Tenders", f"{total_tenders:,}"),
    (k2, "kpi-green", "🟢", "Active Tenders", f"{active_count:,}"),
    (k3, "kpi-orange", "📍", "Districts", f"{dist_count:,}"),
    (k4, "kpi-purple", "🏢", "Departments", f"{dept_count:,}"),
    (k5, "kpi-cyan", "💰", "Tender Value", f"₹{total_value:,.0f}"),
]

for col, css_class, icon, label, value in cards:
    with col:
        st.markdown(
            f"""
            <div class="kpi-card {css_class}">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# STATUS BAR
# ============================================================
result_col, portal_col, updated_col = st.columns([2, 1, 1])

with result_col:
    st.info(
        f"🔎 Showing **{len(filtered_df):,}** matching tenders"
        + (f" from **{len(df):,}** total records." if len(df) != len(filtered_df) else ".")
    )

with portal_col:
    st.metric("Portals in View", portal_count)

with updated_col:
    st.metric("Dataset Records", len(df))


# ============================================================
# TABS
# ============================================================
# Swapped the order to put Tender Records first
tab1, tab2 = st.tabs(["🗃️ Tender Records", "📊 Analytics"])

# ============================================================
# RECORDS TAB (Now Tab 1)
# ============================================================
with tab1:

    left, right = st.columns([3, 1])

    with left:
        st.markdown(
            f'<div class="section-title">🗂️ Tender Records <span style="color:#64748b;font-weight:500;">({len(filtered_df):,})</span></div>',
            unsafe_allow_html=True,
        )

    with right:
        st.download_button(
            "⬇️ Export CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_odisha_tenders.csv",
            mime="text/csv",
            use_container_width=True,
        )

    cols_to_hide = ["State", "Source Portal"]
    display_df = (
        filtered_df
        .drop(columns=cols_to_hide, errors="ignore")
        .dropna(axis=1, how="all")
    )

    column_configs = {}

    if "Link" in display_df.columns:
        column_configs["Link"] = st.column_config.LinkColumn(
            "Document",
            display_text="🔗 Open Tender",
        )

    if "Summary" in display_df.columns:
        column_configs["Summary"] = st.column_config.TextColumn(
            "Summary",
            help="Click the cell to inspect the tender summary.",
            width="large",
        )

    if "Published Date" in display_df.columns:
        column_configs["Published Date"] = st.column_config.DatetimeColumn(
            "Published",
            format="DD MMM YYYY",
        )

    if "Opening Date" in display_df.columns:
        column_configs["Opening Date"] = st.column_config.DatetimeColumn(
            "Opening",
            format="DD MMM YYYY",
        )

    if "Closing Date" in display_df.columns:
        column_configs["Closing Date"] = st.column_config.DatetimeColumn(
            "Closing",
            format="DD MMM YYYY",
        )

    if "Tender Value" in display_df.columns:
        column_configs["Tender Value"] = st.column_config.NumberColumn(
            "Tender Value",
            format="₹ %.0f",
        )

    st.dataframe(
        display_df,
        column_config=column_configs,
        hide_index=True,
        use_container_width=True,
        height=620,
        selection_mode="single-row",
        on_select="ignore",
    )

# ============================================================
# ANALYTICS TAB (Now Tab 2)
# ============================================================
with tab2:

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if "District" in filtered_df.columns and not filtered_df.empty:
            dist_counts = (
                filtered_df["District"]
                .value_counts()
                .head(10)
                .reset_index()
            )
            dist_counts.columns = ["District", "Tender Count"]

            fig_bar = px.bar(
                dist_counts,
                x="District",
                y="Tender Count",
                title="Top Districts by Tender Volume",
                template="plotly_white",
                text_auto=True,
            )

            fig_bar.update_traces(
                marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Tenders: %{y}<extra></extra>",
            )

            fig_bar.update_layout(
                showlegend=False,
                height=390,
                margin=dict(t=65, b=45, l=20, r=20),
                title_font=dict(size=18),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        if "Department" in filtered_df.columns and not filtered_df.empty:
            dept_counts = (
                filtered_df["Department"]
                .value_counts()
                .head(8)
                .reset_index()
            )
            dept_counts.columns = ["Department", "Count"]

            fig_pie = px.pie(
                dept_counts,
                values="Count",
                names="Department",
                hole=0.55,
                title="Department Distribution",
                template="plotly_white",
            )

            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent",
            )

            fig_pie.update_layout(
                height=390,
                margin=dict(t=65, b=30, l=10, r=10),
                title_font=dict(size=18),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Portal + closing trend
    lower1, lower2 = st.columns(2)

    with lower1:
        if "Source Portal" in filtered_df.columns and not filtered_df.empty:
            portal_counts = (
                filtered_df["Source Portal"]
                .value_counts()
                .reset_index()
            )
            portal_counts.columns = ["Source Portal", "Tender Count"]

            fig_portal = px.bar(
                portal_counts,
                x="Tender Count",
                y="Source Portal",
                orientation="h",
                title="Tenders by Source Portal",
                template="plotly_white",
                text_auto=True,
            )

            fig_portal.update_layout(
                height=320,
                margin=dict(t=65, b=25, l=20, r=20),
                title_font=dict(size=18),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_portal, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with lower2:
        if "Closing Date" in filtered_df.columns and not filtered_df.empty:
            closing_trend = (
                filtered_df.dropna(subset=["Closing Date"])
                .assign(ClosingDay=lambda x: x["Closing Date"].dt.date)
                .groupby("ClosingDay")
                .size()
                .reset_index(name="Tender Count")
            )

            if not closing_trend.empty:
                fig_close = px.area(
                    closing_trend,
                    x="ClosingDay",
                    y="Tender Count",
                    title="Tender Closing Activity",
                    template="plotly_white",
                )

                fig_close.update_layout(
                    height=320,
                    margin=dict(t=65, b=25, l=20, r=20),
                    title_font=dict(size=18),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_close, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        Tender Intelligence Platform • Odisha • Built for faster tender discovery
    </div>
    """,
    unsafe_allow_html=True,
)