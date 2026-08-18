import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tender Intelligence Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN PAGE
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37, 99, 235, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(14, 165, 233, 0.07),
                transparent 25%
            ),
            #f5f7fb;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1500px;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 100%
        );

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.09) !important;
        border-color: rgba(255,255,255,0.16) !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.09) !important;
        border-color: rgba(255,255,255,0.16) !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] .stDateInput input {
        background: rgba(255,255,255,0.09) !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 26px 30px 25px;

        border-radius: 20px;

        margin-bottom: 20px;

        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #1e3a8a 55%,
                #0369a1 100%
            );

        color: white;

        box-shadow:
            0 14px 35px rgba(15, 23, 42, 0.18);
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


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        font-size: 1.05rem;

        font-weight: 800;

        color: #0f172a;

        margin: 8px 0 12px;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {
        position: relative;

        background: rgba(255,255,255,0.96);

        border: 1px solid #e5e7eb;

        border-radius: 16px;

        padding: 16px 18px;

        min-height: 108px;

        box-shadow:
            0 7px 20px rgba(15,23,42,0.06);

        transition: all .2s ease;

        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-3px);

        box-shadow:
            0 13px 28px rgba(15,23,42,0.11);
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
        font-size: 1.7rem;

        line-height: 1.2;

        color: #0f172a;

        font-weight: 800;

        margin-top: 3px;
    }

    .kpi-blue {
        border-top: 4px solid #2563eb;
    }

    .kpi-green {
        border-top: 4px solid #16a34a;
    }

    .kpi-orange {
        border-top: 4px solid #f59e0b;
    }

    .kpi-purple {
        border-top: 4px solid #7c3aed;
    }

    .kpi-cyan {
        border-top: 4px solid #0891b2;
    }


    /* ========================================================
       TABS
       ======================================================== */

    div[data-baseweb="tab-list"] {
        background: #ffffff !important;

        border: 1px solid #dbe3ef !important;

        border-radius: 14px !important;

        padding: 5px !important;

        margin-top: 8px !important;
        margin-bottom: 15px !important;

        box-shadow:
            0 6px 18px rgba(15,23,42,0.06) !important;
    }

    button[data-baseweb="tab"] {
        color: #334155 !important;

        font-weight: 800 !important;

        font-size: 0.95rem !important;

        border-radius: 10px !important;

        opacity: 1 !important;

        visibility: visible !important;

        padding: 10px 20px !important;
    }

    button[data-baseweb="tab"] p {
        color: #334155 !important;

        font-weight: 800 !important;

        opacity: 1 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1d4ed8 !important;

        background: #eff6ff !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #1d4ed8 !important;
    }


    /* ========================================================
       CHART CARD
       ======================================================== */

    .chart-card {
        background: white;

        border: 1px solid #e5e7eb;

        border-radius: 16px;

        padding: 8px 10px 2px;

        box-shadow:
            0 7px 20px rgba(15,23,42,0.05);
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 7px 20px rgba(15,23,42,0.05);
    }


    /* ========================================================
       ALERT / INFO
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.75rem;

        margin-top: 25px;

        padding-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=600)
def load_data():

    file_path = "odisha_tenders.xlsx"

    if not os.path.exists(file_path):
        file_path = "odisha_tenders_20260814_122122.xlsx"

    try:

        df = pd.read_excel(file_path)

        # ----------------------------------------------------
        # Tender Value
        # ----------------------------------------------------

        if "Tender Value" in df.columns:

            df["Tender Value"] = pd.to_numeric(
                df["Tender Value"],
                errors="coerce"
            ).fillna(0)


        # ----------------------------------------------------
        # Date Columns
        # ----------------------------------------------------

        for date_col in [
            "Published Date",
            "Opening Date",
            "Closing Date"
        ]:

            if date_col in df.columns:

                df[date_col] = pd.to_datetime(
                    df[date_col],
                    errors="coerce"
                )


        # ----------------------------------------------------
        # Identify Source Portal
        # ----------------------------------------------------

        if "Tender No" in df.columns:

            def identify_source(tender_no):

                tender_no = str(
                    tender_no
                ).strip().upper()

                if tender_no.startswith("GEM"):
                    return "GeM"

                return "NIC / State Portal"


            source_index = (
                df.columns.get_loc("Tender No") + 1
            )

            df.insert(
                source_index,
                "Source Portal",
                df["Tender No"].apply(
                    identify_source
                )
            )


        # ----------------------------------------------------
        # Tender Links
        # ----------------------------------------------------

        def get_valid_link(row):

            link = str(
                row.get("Link", "")
            ).strip()

            tender_no = str(
                row.get("Tender No", "")
            ).strip()


            if link.startswith("http"):
                return link


            if tender_no.upper().startswith("GEM"):

                return (
                    "https://bidplus.gem.gov.in/"
                    f"all-bids?q={tender_no}"
                )


            return (
                "https://tenders.odisha.gov.in"
            )


        if "Link" in df.columns:

            df["Link"] = df.apply(
                get_valid_link,
                axis=1
            )

        else:

            df["Link"] = (
                "https://bidplus.gem.gov.in/all-bids"
            )


        return df


    except Exception as e:

        st.error(
            f"Failed to load Excel file: {e}"
        )

        return pd.DataFrame()


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if df.empty:

    st.warning(
        "No tender data found. "
        "Please ensure the Excel file exists "
        "in the same folder as this Streamlit app."
    )

    st.stop()


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-kicker">
            Odisha Government Procurement
        </div>

        <div class="hero-title">
            🏛️ Tender Intelligence Dashboard
        </div>

        <div class="hero-subtitle">
            Search, filter and analyse government tenders
            from multiple Odisha portals in one place.
        </div>

        <div class="hero-badge">
            ● Live dataset • Intelligent filtering • Tender tracking
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "## 🎯 Tender Filters"
)

st.sidebar.caption(
    "Find the government tender opportunities "
    "you are looking for."
)


# ============================================================
# SEARCH
# ============================================================

search_query = st.sidebar.text_input(
    "🔎 Search",

    placeholder=(
        "Tender title, ID or keyword..."
    )
)


# ============================================================
# SOURCE PORTAL
# ============================================================

if "Source Portal" in df.columns:

    sources = sorted(
        [
            str(x)
            for x in df["Source Portal"]
            .dropna()
            .unique()
            if str(x).strip()
        ]
    )

    selected_sources = st.sidebar.multiselect(
        "🌐 Source Portal",
        options=sources
    )

else:

    selected_sources = []


# ============================================================
# DISTRICT
# ============================================================

if "District" in df.columns:

    districts = sorted(
        [
            str(x)
            for x in df["District"]
            .dropna()
            .unique()
            if str(x).strip()
        ]
    )

    selected_districts = st.sidebar.multiselect(
        "📍 District",
        options=districts
    )

else:

    selected_districts = []


# ============================================================
# DEPARTMENT
# ============================================================

if "Department" in df.columns:

    departments = sorted(
        [
            str(x)
            for x in df["Department"]
            .dropna()
            .unique()
            if str(x).strip()
        ]
    )

    selected_departments = st.sidebar.multiselect(
        "🏢 Department",
        options=departments
    )

else:

    selected_departments = []


# ============================================================
# DATE FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 📅 Date Filters"
)

st.sidebar.caption(
    "The complete dataset is shown by default. "
    "Change a date range only when you want to filter."
)


# ------------------------------------------------------------
# Published Date Range
# ------------------------------------------------------------

selected_pub_date = []

min_pub = None
max_pub = None


if (
    "Published Date" in df.columns
    and not df["Published Date"]
        .dropna()
        .empty
):

    min_pub = (
        df["Published Date"]
        .min()
        .date()
    )

    max_pub = (
        df["Published Date"]
        .max()
        .date()
    )


    selected_pub_date = st.sidebar.date_input(

        "Published Date",

        value=(
            min_pub,
            max_pub
        ),

        min_value=min_pub,

        max_value=max_pub,

        key="published_date_filter"

    )


# ------------------------------------------------------------
# Closing Date Range
# ------------------------------------------------------------

selected_close_date = []

min_close = None
max_close = None


if (
    "Closing Date" in df.columns
    and not df["Closing Date"]
        .dropna()
        .empty
):

    min_close = (
        df["Closing Date"]
        .min()
        .date()
    )

    max_close = (
        df["Closing Date"]
        .max()
        .date()
    )


    selected_close_date = st.sidebar.date_input(

        "Closing Date",

        value=(
            min_close,
            max_close
        ),

        min_value=min_close,

        max_value=max_close,

        key="closing_date_filter"

    )


st.sidebar.markdown("---")

st.sidebar.caption(
    "💡 Tip: Combine portal, district and department "
    "filters to quickly find relevant opportunities."
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# ============================================================
# SEARCH FILTER
# ============================================================

if search_query:

    search_mask = pd.Series(
        False,
        index=filtered_df.index
    )


    if "Title" in filtered_df.columns:

        search_mask |= (
            filtered_df["Title"]
            .astype(str)
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        )


    if "Tender No" in filtered_df.columns:

        search_mask |= (
            filtered_df["Tender No"]
            .astype(str)
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        )


    if "Summary" in filtered_df.columns:

        search_mask |= (
            filtered_df["Summary"]
            .astype(str)
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        )


    filtered_df = filtered_df[
        search_mask
    ]


# ============================================================
# SOURCE FILTER
# ============================================================

if selected_sources:

    filtered_df = filtered_df[
        filtered_df["Source Portal"]
        .isin(selected_sources)
    ]


# ============================================================
# DISTRICT FILTER
# ============================================================

if selected_districts:

    filtered_df = filtered_df[
        filtered_df["District"]
        .isin(selected_districts)
    ]


# ============================================================
# DEPARTMENT FILTER
# ============================================================

if selected_departments:

    filtered_df = filtered_df[
        filtered_df["Department"]
        .isin(selected_departments)
    ]


# ============================================================
# PUBLISHED DATE FILTER
# ============================================================
#
# IMPORTANT:
#
# On initial load:
#
#   min date → max date
#
# Therefore the date filter is NOT applied.
#
# This keeps all 203 records visible.
#
# Only when the user changes the date range do we filter.
#
# ============================================================

if (
    len(selected_pub_date) == 2
    and min_pub is not None
    and max_pub is not None
):

    start_pub = selected_pub_date[0]
    end_pub = selected_pub_date[1]


    if (
        start_pub != min_pub
        or end_pub != max_pub
    ):

        filtered_df = filtered_df[
            filtered_df["Published Date"].notna()
            &
            (
                filtered_df["Published Date"]
                .dt.date
                >= start_pub
            )
            &
            (
                filtered_df["Published Date"]
                .dt.date
                <= end_pub
            )
        ]


# ============================================================
# CLOSING DATE FILTER
# ============================================================

if (
    len(selected_close_date) == 2
    and min_close is not None
    and max_close is not None
):

    start_close = selected_close_date[0]
    end_close = selected_close_date[1]


    if (
        start_close != min_close
        or end_close != max_close
    ):

        filtered_df = filtered_df[
            filtered_df["Closing Date"].notna()
            &
            (
                filtered_df["Closing Date"]
                .dt.date
                >= start_close
            )
            &
            (
                filtered_df["Closing Date"]
                .dt.date
                <= end_close
            )
        ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_tenders = len(
    filtered_df
)

today = datetime.now().date()

active_count = 0


# ============================================================
# ACTIVE TENDERS
# ============================================================

if not filtered_df.empty:

    is_opened = pd.Series(
        True,
        index=filtered_df.index
    )


    # --------------------------------------------------------
    # Opening Date
    # --------------------------------------------------------

    if "Opening Date" in filtered_df.columns:

        is_opened = (
            filtered_df["Opening Date"]
            .dt.date
            <= today
        )


        if "Published Date" in filtered_df.columns:

            is_opened |= (
                filtered_df["Opening Date"].isna()
                &
                (
                    filtered_df["Published Date"]
                    .dt.date
                    <= today
                )
            )


    # --------------------------------------------------------
    # Closing Date
    # --------------------------------------------------------

    if "Closing Date" in filtered_df.columns:

        is_active = (
            is_opened
            &
            (
                filtered_df["Closing Date"].isna()
                |
                (
                    filtered_df["Closing Date"]
                    .dt.date
                    >= today
                )
            )
        )

        active_count = int(
            is_active.sum()
        )

    else:

        active_count = int(
            is_opened.sum()
        )


# ============================================================
# OTHER KPIs
# ============================================================

if "District" in filtered_df.columns:

    district_count = (
        filtered_df["District"]
        .nunique()
    )

else:

    district_count = 0


if "Department" in filtered_df.columns:

    department_count = (
        filtered_df["Department"]
        .nunique()
    )

else:

    department_count = 0


if "Source Portal" in filtered_df.columns:

    portal_count = (
        filtered_df["Source Portal"]
        .nunique()
    )

else:

    portal_count = 0


if "Tender Value" in filtered_df.columns:

    total_value = (
        filtered_df["Tender Value"]
        .sum()
    )

else:

    total_value = 0


# ============================================================
# KPI HEADER
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📌 Opportunity Snapshot'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)


kpi_data = [

    (
        k1,
        "kpi-blue",
        "📋",
        "Total Tenders",
        f"{total_tenders:,}"
    ),

    (
        k2,
        "kpi-green",
        "🟢",
        "Active Tenders",
        f"{active_count:,}"
    ),

    (
        k3,
        "kpi-orange",
        "📍",
        "Districts",
        f"{district_count:,}"
    ),

    (
        k4,
        "kpi-purple",
        "🏢",
        "Departments",
        f"{department_count:,}"
    ),

    (
        k5,
        "kpi-cyan",
        "💰",
        "Tender Value",
        f"₹{total_value:,.0f}"
    )

]


for (
    column,
    css_class,
    icon,
    label,
    value
) in kpi_data:

    with column:

        st.markdown(
            f"""
            <div class="kpi-card {css_class}">

                <div class="kpi-icon">
                    {icon}
                </div>

                <div class="kpi-label">
                    {label}
                </div>

                <div class="kpi-value">
                    {value}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# ============================================================
# MATCHING RESULT
# ============================================================

result_col, portal_col, total_col = st.columns(
    [2, 1, 1]
)


with result_col:

    if len(filtered_df) == len(df):

        st.info(
            f"🔎 Showing **{len(filtered_df):,}** "
            "matching tenders from the complete dataset."
        )

    else:

        st.info(
            f"🔎 Showing **{len(filtered_df):,}** "
            f"matching tenders from "
            f"**{len(df):,}** total records."
        )


with portal_col:

    st.metric(
        "Portals in View",
        portal_count
    )


with total_col:

    st.metric(
        "Total Records",
        len(df)
    )


# ============================================================
# TABS
# ============================================================
#
# FIRST  = Tender Records
# SECOND = Analytics
#
# ============================================================

tab_records, tab_analytics = st.tabs(
    [
        "🗃️ Tender Records",
        "📊 Analytics"
    ]
)


# ============================================================
# TAB 1
# TENDER RECORDS
# ============================================================

with tab_records:

    st.markdown(
        f"""
        <div class="section-title">

            🗂️ Tender Records

            <span
                style="
                    color:#64748b;
                    font-weight:500;
                "
            >
                ({len(filtered_df):,})
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Hide Columns
    # --------------------------------------------------------

    columns_to_hide = [
        "State",
        "Source Portal"
    ]


    display_df = (
        filtered_df
        .drop(
            columns=columns_to_hide,
            errors="ignore"
        )
        .dropna(
            axis=1,
            how="all"
        )
    )


    # --------------------------------------------------------
    # Column Configuration
    # --------------------------------------------------------

    column_configs = {}


    # --------------------------------------------------------
    # Link
    # --------------------------------------------------------

    if "Link" in display_df.columns:

        column_configs["Link"] = (
            st.column_config.LinkColumn(
                "Document",
                display_text="🔗 Open Tender"
            )
        )


    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if "Summary" in display_df.columns:

        column_configs["Summary"] = (
            st.column_config.TextColumn(
                "Summary",
                help=(
                    "Click the cell to inspect "
                    "the complete tender summary."
                ),
                width="large"
            )
        )


    # --------------------------------------------------------
    # Published Date
    # --------------------------------------------------------

    if "Published Date" in display_df.columns:

        column_configs["Published Date"] = (
            st.column_config.DatetimeColumn(
                "Published",
                format="DD MMM YYYY"
            )
        )


    # --------------------------------------------------------
    # Opening Date
    # --------------------------------------------------------

    if "Opening Date" in display_df.columns:

        column_configs["Opening Date"] = (
            st.column_config.DatetimeColumn(
                "Opening",
                format="DD MMM YYYY"
            )
        )


    # --------------------------------------------------------
    # Closing Date
    # --------------------------------------------------------

    if "Closing Date" in display_df.columns:

        column_configs["Closing Date"] = (
            st.column_config.DatetimeColumn(
                "Closing",
                format="DD MMM YYYY"
            )
        )


    # --------------------------------------------------------
    # Tender Value
    # --------------------------------------------------------

    if "Tender Value" in display_df.columns:

        column_configs["Tender Value"] = (
            st.column_config.NumberColumn(
                "Tender Value",
                format="₹ %.0f"
            )
        )


    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    st.dataframe(

        display_df,

        column_config=column_configs,

        hide_index=True,

        use_container_width=True,

        height=620,

        selection_mode="single-row",

        on_select="ignore"

    )


# ============================================================
# TAB 2
# ANALYTICS
# ============================================================

with tab_analytics:

    st.markdown(
        '<div class="section-title">'
        '📊 Tender Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # TOP CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)


    # ========================================================
    # DISTRICT CHART
    # ========================================================

    with chart_col1:

        if (
            "District" in filtered_df.columns
            and not filtered_df.empty
        ):

            district_counts = (
                filtered_df["District"]
                .value_counts()
                .head(10)
                .reset_index()
            )


            district_counts.columns = [
                "District",
                "Tender Count"
            ]


            fig_district = px.bar(

                district_counts,

                x="District",

                y="Tender Count",

                title=(
                    "Top Districts "
                    "by Tender Volume"
                ),

                template="plotly_white",

                text_auto=True

            )


            fig_district.update_traces(

                marker_line_width=0,

                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>"
                    "Tenders: %{y}"
                    "<extra></extra>"
                )

            )


            fig_district.update_layout(

                showlegend=False,

                height=390,

                margin=dict(
                    t=65,
                    b=45,
                    l=20,
                    r=20
                ),

                title_font=dict(
                    size=18
                ),

                paper_bgcolor=(
                    "rgba(0,0,0,0)"
                ),

                plot_bgcolor=(
                    "rgba(0,0,0,0)"
                )

            )


            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True
            )


            st.plotly_chart(
                fig_district,
                use_container_width=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


    # ========================================================
    # DEPARTMENT CHART
    # ========================================================

    with chart_col2:

        if (
            "Department" in filtered_df.columns
            and not filtered_df.empty
        ):

            department_counts = (
                filtered_df["Department"]
                .value_counts()
                .head(8)
                .reset_index()
            )


            department_counts.columns = [
                "Department",
                "Count"
            ]


            fig_department = px.pie(

                department_counts,

                values="Count",

                names="Department",

                hole=0.55,

                title="Department Distribution",

                template="plotly_white"

            )


            fig_department.update_traces(

                textposition="inside",

                textinfo="percent"

            )


            fig_department.update_layout(

                height=390,

                margin=dict(
                    t=65,
                    b=30,
                    l=10,
                    r=10
                ),

                title_font=dict(
                    size=18
                ),

                legend=dict(

                    orientation="h",

                    yanchor="bottom",

                    y=-0.25,

                    xanchor="center",

                    x=0.5

                ),

                paper_bgcolor=(
                    "rgba(0,0,0,0)"
                ),

                plot_bgcolor=(
                    "rgba(0,0,0,0)"
                )

            )


            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True
            )


            st.plotly_chart(
                fig_department,
                use_container_width=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


    # ========================================================
    # LOWER CHARTS
    # ========================================================

    lower_col1, lower_col2 = st.columns(2)


    # ========================================================
    # SOURCE PORTAL
    # ========================================================

    with lower_col1:

        if (
            "Source Portal" in filtered_df.columns
            and not filtered_df.empty
        ):

            portal_counts = (
                filtered_df["Source Portal"]
                .value_counts()
                .reset_index()
            )


            portal_counts.columns = [
                "Source Portal",
                "Tender Count"
            ]


            fig_portal = px.bar(

                portal_counts,

                x="Tender Count",

                y="Source Portal",

                orientation="h",

                title="Tenders by Source Portal",

                template="plotly_white",

                text_auto=True

            )


            fig_portal.update_layout(

                height=320,

                margin=dict(
                    t=65,
                    b=25,
                    l=20,
                    r=20
                ),

                title_font=dict(
                    size=18
                ),

                paper_bgcolor=(
                    "rgba(0,0,0,0)"
                ),

                plot_bgcolor=(
                    "rgba(0,0,0,0)"
                )

            )


            st.markdown(
                '<div class="chart-card">',
                unsafe_allow_html=True
            )


            st.plotly_chart(
                fig_portal,
                use_container_width=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


    # ========================================================
    # CLOSING ACTIVITY
    # ========================================================

    with lower_col2:

        if (
            "Closing Date" in filtered_df.columns
            and not filtered_df.empty
        ):

            closing_data = (
                filtered_df
                .dropna(
                    subset=["Closing Date"]
                )
                .copy()
            )


            if not closing_data.empty:

                closing_data["Closing Day"] = (
                    closing_data["Closing Date"]
                    .dt.date
                )


                closing_trend = (
                    closing_data
                    .groupby("Closing Day")
                    .size()
                    .reset_index(
                        name="Tender Count"
                    )
                )


                fig_closing = px.area(

                    closing_trend,

                    x="Closing Day",

                    y="Tender Count",

                    title="Tender Closing Activity",

                    template="plotly_white"

                )


                fig_closing.update_layout(

                    height=320,

                    margin=dict(
                        t=65,
                        b=25,
                        l=20,
                        r=20
                    ),

                    title_font=dict(
                        size=18
                    ),

                    paper_bgcolor=(
                        "rgba(0,0,0,0)"
                    ),

                    plot_bgcolor=(
                        "rgba(0,0,0,0)"
                    )

                )


                st.markdown(
                    '<div class="chart-card">',
                    unsafe_allow_html=True
                )


                st.plotly_chart(
                    fig_closing,
                    use_container_width=True
                )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        Tender Intelligence Platform • Odisha

        <br>

        Built for faster government tender discovery

    </div>
    """,
    unsafe_allow_html=True
)