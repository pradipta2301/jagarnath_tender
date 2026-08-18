import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tender Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS INJECTION ---
st.markdown("""
<style>
    /* 1. Reduce Top Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        margin-top: 0 !important;
    }
    
    /* Centered Header Styles */
    .dashboard-header {
        text-align: center;
        padding-bottom: 5px;
        margin-bottom: 10px;
        margin-top: -10px;
        border-bottom: 1px solid rgba(128,128,128, 0.2);
    }
    .dashboard-header h1 {
        margin-bottom: 0px;
        font-weight: 700;
        font-size: 2.2rem;
    }
    .dashboard-header p {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 5px;
    }
    
    /* 2. Custom KPI Card Styles (COMPACT MODE) */
    .kpi-card {
        background-color: #FFF4E6;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 165, 0, 0.3);
        text-align: left;
        min-height: 65px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #555;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: #212529;
        margin: 0;
        line-height: 1.2;
    }
    
    /* Left border accents */
    .kpi-blue { border-left: 5px solid #0078D4; }
    .kpi-green { border-left: 5px solid #107C41; }
    .kpi-orange { border-left: 5px solid #D83B01; }
    .kpi-purple { border-left: 5px solid #5C2D91; }
    
    /* 3. Table Header Styling via CSS */
    thead tr th {
        background-color: #E6E6FA !important;
        color: black !important;
        font-weight: bold !important;
    }
    
    /* 4. Force Tabs to be always visible and bold */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1E1E1E !important; /* Dark text for visibility */
    }
    .stTabs [data-baseweb="tab-list"] button {
        opacity: 1 !important; /* Prevent Streamlit from dimming inactive tabs */
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: #0078D4 !important; /* Blue underline for active tab */
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #0078D4 !important; /* Blue text for active tab */
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(ttl=600)
def load_data():
    file_path = "odisha_tenders.xlsx"
    if not os.path.exists(file_path):
        file_path = "odisha_tenders_20260814_122122.xlsx"
        
    try:
        df = pd.read_excel(file_path)
        
        if 'Tender Value' in df.columns:
            df['Tender Value'] = pd.to_numeric(df['Tender Value'], errors='coerce').fillna(0)
            
        for date_col in ['Published Date', 'Opening Date', 'Closing Date']:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        if 'Tender No' in df.columns:
            def identify_source(t_no):
                t_no_str = str(t_no).strip().upper()
                if t_no_str.startswith('GEM'):
                    return 'GeM'
                else:
                    return 'NIC / State Portal'
            
            idx = df.columns.get_loc('Tender No') + 1 if 'Tender No' in df.columns else len(df.columns)
            df.insert(idx, 'Source Portal', df['Tender No'].apply(identify_source))

        def get_valid_link(row):
            link = str(row.get('Link', '')).strip()
            t_no = str(row.get('Tender No', '')).strip()
            
            if link.startswith('http'):
                return link
            if t_no.startswith('GEM'):
                return f"https://bidplus.gem.gov.in/all-bids?q={t_no}"
            else:
                return "https://tenders.odisha.gov.in"

        if 'Link' in df.columns:
            df['Link'] = df.apply(get_valid_link, axis=1)
        else:
            df['Link'] = "https://gem.gov.in"
            
        return df
    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data found. Please ensure the Excel file exists in the same folder.")
else:
    # --- CENTERED HEADER ---
    st.markdown("""
        <div class="dashboard-header">
            <h1>🏢 Tender Intelligence Dashboard</h1>
            <p>Advanced analytics and tracking for active government tenders in Odisha.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Filter Parameters")
    
    search_query = st.sidebar.text_input("Search (Title, ID, Summary)")
    
    if 'Source Portal' in df.columns:
        sources = [d for d in df['Source Portal'].dropna().unique().tolist() if str(d).strip() != ""]
        selected_sources = st.sidebar.multiselect("Source Website", options=sorted(sources))
    else:
        selected_sources = []

    if 'District' in df.columns:
        districts = [d for d in df['District'].dropna().unique().tolist() if str(d).strip() != ""]
        selected_districts = st.sidebar.multiselect("Select District", options=sorted(districts))
    else:
        selected_districts = []

    if 'Department' in df.columns:
        depts = [d for d in df['Department'].dropna().unique().tolist() if str(d).strip() != ""]
        selected_depts = st.sidebar.multiselect("Select Department", options=sorted(depts))
    else:
        selected_depts = []

    # Safe Date Defaults
    st.sidebar.markdown("### 📅 Date Filters")
    st.sidebar.caption("Select a Start and End date for ranges.")
    
    selected_pub_date = []
    min_pub, max_pub = None, None
    if 'Published Date' in df.columns and not df['Published Date'].dropna().empty:
        min_pub = df['Published Date'].min().date()
        max_pub = df['Published Date'].max().date()
        # Default precisely covers ALL records so nothing is hidden initially
        selected_pub_date = st.sidebar.date_input("Published Date Range", value=(min_pub, max_pub), min_value=min_pub, max_value=max_pub)

    selected_close_date = []
    min_close, max_close = None, None
    if 'Closing Date' in df.columns and not df['Closing Date'].dropna().empty:
        min_close = df['Closing Date'].min().date()
        max_close = df['Closing Date'].max().date()
        selected_close_date = st.sidebar.date_input("Closing Date Range", value=(min_close, max_close), min_value=min_close, max_value=max_close)

    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    
    if search_query:
        search_mask = (
            filtered_df['Title'].str.contains(search_query, case=False, na=False) |
            filtered_df['Tender No'].str.contains(search_query, case=False, na=False)
        )
        if 'Summary' in filtered_df.columns:
            search_mask |= filtered_df['Summary'].str.contains(search_query, case=False, na=False)
        filtered_df = filtered_df[search_mask]
        
    if selected_sources:
        filtered_df = filtered_df[filtered_df['Source Portal'].isin(selected_sources)]
    if selected_districts:
        filtered_df = filtered_df[filtered_df['District'].isin(selected_districts)]
    if selected_depts:
        filtered_df = filtered_df[filtered_df['Department'].isin(selected_depts)]
        
    # Only drop rows if the user actually changed the date from the absolute min/max defaults
    if len(selected_pub_date) == 2:
        start_pub, end_pub = selected_pub_date
        if start_pub != min_pub or end_pub != max_pub:
            filtered_df = filtered_df[
                (filtered_df['Published Date'].dt.date >= start_pub) & 
                (filtered_df['Published Date'].dt.date <= end_pub)
            ]
            
    if len(selected_close_date) == 2:
        start_close, end_close = selected_close_date
        if start_close != min_close or end_close != max_close:
            filtered_df = filtered_df[
                (filtered_df['Closing Date'].dt.date >= start_close) & 
                (filtered_df['Closing Date'].dt.date <= end_close)
            ]

    # --- TOP METRIC CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_tenders = len(filtered_df)
    
    today = datetime.now().date()
    active_count = 0
    if not filtered_df.empty:
        is_opened = pd.Series(True, index=filtered_df.index)
        if 'Opening Date' in filtered_df.columns and 'Published Date' in filtered_df.columns:
            is_opened = (filtered_df['Opening Date'].dt.date <= today) | (filtered_df['Opening Date'].isna() & (filtered_df['Published Date'].dt.date <= today))
            
        if 'Closing Date' in filtered_df.columns:
            is_active = is_opened & (filtered_df['Closing Date'].isna() | (filtered_df['Closing Date'].dt.date >= today))
            active_count = len(filtered_df[is_active])
        else:
            active_count = len(filtered_df[is_opened])
    
    dist_count = filtered_df['District'].nunique() if 'District' in filtered_df.columns else 0
    dept_count = filtered_df['Department'].nunique() if 'Department' in filtered_df.columns else 0

    with col1:
        st.markdown(f"""
            <div class="kpi-card kpi-blue">
                <div class="kpi-label">Total Tenders</div>
                <div class="kpi-value">{total_tenders}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="kpi-card kpi-green">
                <div class="kpi-label">Total Active Tenders</div>
                <div class="kpi-value">{active_count}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="kpi-card kpi-orange">
                <div class="kpi-label">Districts Covered</div>
                <div class="kpi-value">{dist_count}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class="kpi-card kpi-purple">
                <div class="kpi-label">Active Departments</div>
                <div class="kpi-value">{dept_count}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TABS (SWAPPED ORDER) ---
    tab1, tab2 = st.tabs(["🗃️ Tender Records", "📈 Analytics"])

    with tab1:
        cols_to_hide = ['State', 'Source Portal']
        display_df = filtered_df.drop(columns=cols_to_hide, errors='ignore').dropna(axis=1, how='all')
        
        column_configs = {}
        
        if 'Link' in display_df.columns:
            column_configs['Link'] = st.column_config.LinkColumn("Document Link", display_text="View PDF 🔗")
            
        if 'Summary' in display_df.columns:
            column_configs['Summary'] = st.column_config.TextColumn("Summary", help="Click cell to expand and read full summary.")

        if 'Published Date' in display_df.columns:
            column_configs['Published Date'] = st.column_config.DatetimeColumn("Published Date", format="DD MMM YYYY")
            
        if 'Opening Date' in display_df.columns:
            column_configs['Opening Date'] = st.column_config.DatetimeColumn("Opening Date", format="DD MMM YYYY")
            
        if 'Closing Date' in display_df.columns:
            column_configs['Closing Date'] = st.column_config.DatetimeColumn("Closing Date", format="DD MMM YYYY")
            
        st.dataframe(
            display_df,
            column_config=column_configs,
            hide_index=True,
            use_container_width=True,
            height=600,
            selection_mode="single-row",
            on_select="ignore"
        )

    with tab2:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            if 'District' in filtered_df.columns:
                dist_counts = filtered_df['District'].value_counts().head(10).reset_index()
                dist_counts.columns = ['District', 'Tender Count']
                fig_bar = px.bar(
                    dist_counts, x='District', y='Tender Count',
                    color='District', title="Top Districts by Tender Volume",
                    template="plotly_white", color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_bar.update_layout(showlegend=False, margin=dict(t=40, b=40, l=0, r=0))
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with chart_col2:
            if 'Department' in filtered_df.columns:
                dept_counts = filtered_df['Department'].value_counts().head(7).reset_index()
                dept_counts.columns = ['Department', 'Count']
                fig_pie = px.pie(
                    dept_counts, values='Count', names='Department',
                    hole=0.45, title="Department Distribution",
                    template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent')
                fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5), margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig_pie, use_container_width=True)