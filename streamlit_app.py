import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
    
    /* 2. Custom KPI Card Styles (Light Orange with Shadow) */
    .kpi-card {
        background-color: #FFF4E6;
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 165, 0, 0.3);
        text-align: left;
        min-height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
    }
    .kpi-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #555;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
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
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(ttl=600)
def load_data():
    file_path = "odisha_tenders.xlsx" 
    
    try:
        df = pd.read_excel(file_path)
        if 'Tender Value' in df.columns:
            df['Tender Value'] = pd.to_numeric(df['Tender Value'], errors='coerce').fillna(0)
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
    
    search_query = st.sidebar.text_input("Search Tenders...")
    
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

    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains(search_query, case=False, na=False) |
            filtered_df['Tender No'].str.contains(search_query, case=False, na=False)
        ]
    if selected_districts:
        filtered_df = filtered_df[filtered_df['District'].isin(selected_districts)]
    if selected_depts:
        filtered_df = filtered_df[filtered_df['Department'].isin(selected_depts)]

    # --- TOP METRIC CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_val = filtered_df['Tender Value'].sum()
    formatted_val = f"₹ {total_val / 1000000:.2f} M" if total_val > 0 else "N/A"
    
    dist_count = filtered_df['District'].nunique() if 'District' in filtered_df.columns else 0
    dept_count = filtered_df['Department'].nunique() if 'Department' in filtered_df.columns else 0

    with col1:
        st.markdown(f"""
            <div class="kpi-card kpi-blue">
                <div class="kpi-label">Total Opportunities</div>
                <div class="kpi-value">{len(filtered_df)}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="kpi-card kpi-green">
                <div class="kpi-label">Total Value Identified</div>
                <div class="kpi-value">{formatted_val}</div>
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

    # --- TABS ---
    tab1, tab2 = st.tabs(["📈 Executive Summary", "🗃️ Detailed Records"])

    with tab1:
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

    with tab2:
        display_df = filtered_df.dropna(axis=1, how='all')
        
        # Configure clickable links natively
        column_configs = {}
        if 'Link' in display_df.columns:
            column_configs['Link'] = st.column_config.LinkColumn("Document Link", display_text="View PDF 🔗")
            
        st.dataframe(
            display_df,
            column_config=column_configs,
            hide_index=True,
            use_container_width=True,
            height=600
        )