import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
import os
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="MBA 2nd Year 3rd sem",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Clean HTML Renderer to Prevent Markdown Indentation Code Blocks ---
def render_html(html_str):
    cleaned = re.sub(r'^[ \t]+', '', html_str.strip(), flags=re.MULTILINE)
    st.markdown(cleaned, unsafe_allow_html=True)

# --- Course Conducted Mapping ---
COURSE_CONDUCTED = {
    'MBG24301T': 16,
    'MBG24302T': 16,
    'MBG24303L': 24,
    'MBG24B05L': 17,
    'MBG24B06L': 17,
    'MBG24B11L': 17,
    'MBG24F05T': 17,
    'MBG24F09T': 17,
    'MBG24H06T': 17,
    'MBG24H09T': 17,
    'MBG24M07T': 17,
    'MBG24M11T': 17
}

def calculate_attendance_needs(total_conducted, attended, target_pct=75.0):
    p = target_pct / 100.0
    current_pct = (attended / total_conducted) * 100.0 if total_conducted > 0 else 0.0
    if current_pct >= target_pct:
        bunk_buffer = math.floor(attended / p - total_conducted) if p > 0 else 0
        return 0, max(0, bunk_buffer), current_pct
    else:
        num = (p * total_conducted) - attended
        denom = 1.0 - p
        needed = math.ceil(num / denom)
        return max(1, needed), 0, current_pct

# --- Clean Light Theme CSS (Exact Reference Style: No Dark Colors) ---
render_html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>
/* Global Canvas: Clean, Soft Off-White Background */
html, body, .stApp, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: #F4F6FA !important;
    color: #0F172A !important;
}

.main .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 1560px;
    background-color: transparent !important;
}

header[data-testid="stHeader"] {
    background-color: transparent !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Sidebar: Crisp White with Subtle Border */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #EAECF0 !important;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.8rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
}

/* Sidebar Brand */
.mba-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding: 0 4px;
}
.brand-badge {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: #0F172A;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
}
.brand-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.3px;
    line-height: 1.2;
}
.brand-subtitle {
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* Sidebar Menu Radio Button Overrides */
div[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background-color: transparent;
    padding: 10px 14px !important;
    border-radius: 12px !important;
    margin-bottom: 4px !important;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    cursor: pointer;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: #F8FAFC !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"],
div[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: #0F172A !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] p,
div[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Top App Header */
.top-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}
.page-title-text {
    font-size: 1.65rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.4px;
}
.header-badge-sem {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 0.74rem;
    font-weight: 700;
    color: #4F46E5;
    letter-spacing: 0.4px;
    margin-left: 12px;
}
.header-right-tools {
    display: flex;
    align-items: center;
    gap: 12px;
}
.icon-tool-btn {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #475569;
    font-size: 14px;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}
.people-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 13px;
    box-shadow: 0 2px 8px rgba(236, 72, 153, 0.25);
}

/* Clean White Elevated Cards */
.white-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 2px 6px -1px rgba(0, 0, 0, 0.02);
}
.card-header-title {
    font-size: 1.02rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 14px;
    letter-spacing: -0.2px;
}

/* KPI Mini-Cards in Clean Light Theme */
.kpi-mini-card-light {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 14px;
    padding: 16px 8px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-mini-card-light:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}
.kpi-icon-bubble-light {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px auto;
    font-size: 15px;
}
.kpi-mini-label {
    font-size: 0.73rem;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 6px;
}
.kpi-mini-val {
    font-size: 1.55rem;
    font-weight: 800;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}

/* Inner Light Stat Boxes */
.inner-stat-box-light {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px 16px;
}
.inner-stat-label {
    font-size: 0.75rem;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 4px;
}
.inner-stat-val {
    font-size: 1.5rem;
    font-weight: 800;
    color: #2563EB;
    font-family: 'JetBrains Mono', monospace;
}

/* Streamlit Widget Skinning */
div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    color: #0F172A !important;
}
.stSlider > div > div > div > div {
    background: #2563EB !important;
}
button[kind="primary"], .stDownloadButton > button {
    background: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
}
button[kind="primary"]:hover, .stDownloadButton > button:hover {
    background: #1D4ED8 !important;
}
</style>
""")

# --- Load Data ---
@st.cache_data
def load_data():
    file_path = "attendance.csv"
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found.")
        return pd.DataFrame()
    df = pd.read_csv(file_path)
    df['Attendance_Percentage'] = pd.to_numeric(df['Attendance_Percentage'], errors='coerce')
    df['S.No'] = pd.to_numeric(df['S.No'], errors='coerce')
    df['Classes_Conducted'] = df['Course_Code'].map(COURSE_CONDUCTED).fillna(17).astype(int)
    df['Classes_Attended'] = (df['Attendance_Percentage'] * df['Classes_Conducted'] / 100.0).round().astype(int)
    return df

df_raw = load_data()
if df_raw.empty:
    st.stop()

# --- Sidebar UI (MBA 2nd Year 3rd sem Branding) ---
with st.sidebar:
    render_html("""
<div class="mba-brand">
<div class="brand-badge">&#127891;</div>
<div>
<div class="brand-title">MBA 2nd Year 3rd sem</div>
<div class="brand-subtitle">Attendance Portal</div>
</div>
</div>
""")
    
    nav_selection = st.radio(
        "Navigation",
        options=[
            "Dashboard",
            "Reports",
            "Attendance Calculator",
            "Defaulters & Leaves",
            "Master Data",
            "Settings",
            "Help"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    threshold = st.slider(
        "Attendance Benchmark (%):",
        min_value=50,
        max_value=95,
        value=75,
        step=1,
        help="SRM requirement: 75% attendance for examination eligibility."
    )
    
    df = df_raw.copy()
    df['Status'] = df['Attendance_Percentage'].apply(lambda x: 'Shortage' if x < threshold else 'Eligible')
    
    render_html("""
<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:14px; margin-top:20px;">
<div style="font-size:0.75rem; font-weight:800; color:#4F46E5; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">&#9878; Academic Regulation</div>
<div style="font-size:0.78rem; color:#475569; line-height:1.4;">Minimum <b style="color:#0F172A;">75%</b> required per subject to appear in End-Semester examinations.</div>
</div>
""")

# --- Compute Global Metrics ---
total_registrations = len(df)
total_students = df['Register_No'].nunique()
class_avg = df['Attendance_Percentage'].mean()
eligible_count = (df['Attendance_Percentage'] >= threshold).sum()
shortage_count = (df['Attendance_Percentage'] < threshold).sum()
full_100_count = (df['Attendance_Percentage'] == 100.0).sum()
courses_count = df['Course_Code'].nunique()

defaulters_df = df[df['Attendance_Percentage'] < threshold].groupby(['Register_No', 'Student_Name']).agg(
    shortages=('Course_Code', 'count'),
    avg_pct=('Attendance_Percentage', 'mean'),
    lowest_pct=('Attendance_Percentage', 'min'),
    courses=('Course_Code', lambda c: ", ".join(c))
).reset_index().sort_values(by=['shortages', 'lowest_pct'], ascending=[False, True])
defaulters_students_count = len(defaulters_df)
compliant_students_count = total_students - defaulters_students_count

critical_shortage = (df['Attendance_Percentage'] < 50.0).sum()
moderate_shortage = ((df['Attendance_Percentage'] >= 50.0) & (df['Attendance_Percentage'] < threshold)).sum()

# --- Top App Header Row (MBA 2nd Year 3rd sem) ---
render_html(f"""
<div class="top-header-row">
<div style="display:flex; align-items:center;">
<div class="page-title-text">MBA 2nd Year 3rd sem</div>
<span class="header-badge-sem">Batch 2024-2026 &bull; Term III</span>
</div>
<div class="header-right-tools">
<div class="icon-tool-btn" title="Search">&#128269;</div>
<div class="icon-tool-btn" title="Notifications">&#128276;</div>
<div class="people-avatar">MBA</div>
</div>
</div>
""")

# ==============================================================================
# VIEW 1: DASHBOARD (Exact People Layout in Clean Light Theme)
# ==============================================================================
if nav_selection == "Dashboard":
    
    # --------------------------------------------------------------------------
    # ROW 1: STATISTICS DONUT CHART + 6 ATTENDANCE KPI CARDS
    # --------------------------------------------------------------------------
    col_donut, col_kpis = st.columns([1.1, 2.7])
    
    with col_donut:
        render_html("""
<div class="white-card" style="height: 100%;">
<div class="card-header-title">Statistics</div>
""")
        
        # Donut Chart with Clean Ring + Centered Number + Floating Callout
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Eligible (≥75%)', 'Shortage (<75%)', 'Perfect 100%', 'Near Target'],
            values=[eligible_count, shortage_count, full_100_count, 15],
            hole=0.68,
            marker=dict(colors=['#10B981', '#EF4444', '#3B82F6', '#F59E0B']),
            textinfo='none',
            sort=False,
            direction='clockwise'
        )])
        
        fig_donut.add_annotation(
            text=f"<span style='font-size:11px; color:#64748B; font-weight:600;'>Total Students</span><br><b style='font-size:24px; color:#0F172A;'>{total_students}</b>",
            x=0.5, y=0.5,
            showarrow=False,
            align='center'
        )
        
        fig_donut.add_annotation(
            x=0.72, y=0.82,
            text=f"<span style='background:#FFFFFF; border:1px solid #E2E8F0; padding:4px 9px; border-radius:8px; font-size:11px; font-weight:700; color:#0F172A; box-shadow:0 2px 8px rgba(0,0,0,0.06);'><b>{class_avg:.1f}%</b> Checked In</span>",
            showarrow=True,
            arrowhead=0,
            arrowcolor='#94A3B8',
            ax=28, ay=-18
        )
        
        fig_donut.update_layout(
            showlegend=False,
            height=160,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, width='stretch', config={'displayModeBar': False})
        render_html("</div>")

    with col_kpis:
        render_html('<div class="white-card" style="height: 100%;"><div class="card-header-title">Attendance</div>')
        
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        
        with k1:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#E0F2FE; color:#0284C7;">&#10003;</div>
<div class="kpi-mini-label">Checked In</div>
<div class="kpi-mini-val" style="color:#0284C7;">{eligible_count}</div>
</div>
""")
        with k2:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#FEE2E2; color:#EF4444;">&#9888;</div>
<div class="kpi-mini-label">Not Checked In</div>
<div class="kpi-mini-val" style="color:#EF4444;">{shortage_count}</div>
</div>
""")
        with k3:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#DCFCE7; color:#16A34A;">&#9730;</div>
<div class="kpi-mini-label">On Leave</div>
<div class="kpi-mini-val" style="color:#16A34A;">{full_100_count}</div>
</div>
""")
        with k4:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#F3E8FF; color:#9333EA;">&#128197;</div>
<div class="kpi-mini-label">Weekly Off</div>
<div class="kpi-mini-val" style="color:#475569;">{courses_count}</div>
</div>
""")
        with k5:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#FEF3C7; color:#D97706;">&#127873;</div>
<div class="kpi-mini-label">Holiday</div>
<div class="kpi-mini-val" style="color:#D97706;">{defaulters_students_count}</div>
</div>
""")
        with k6:
            render_html(f"""
<div class="kpi-mini-card-light">
<div class="kpi-icon-bubble-light" style="background:#FFEDD5; color:#EA580C;">&#8677;</div>
<div class="kpi-mini-label">Checked Out</div>
<div class="kpi-mini-val" style="color:#EA580C;">{total_students}</div>
</div>
""")
        render_html("</div>")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # ROW 2: ON TIME CHECK IN | OVERTIME | ATTENDANCE SOURCE
    # --------------------------------------------------------------------------
    col_ontime, col_overtime, col_source = st.columns([1.3, 1.3, 1.2])
    
    with col_ontime:
        render_html("""
<div class="white-card" style="height: 100%;">
<div class="card-header-title">On Time Check In</div>
""")
        
        # Bipolar / Diverging Bar Chart vs 75% Benchmark in Light Theme
        c_avg = df.groupby(['Course_Code'])['Attendance_Percentage'].mean().reset_index()
        c_avg['Diff'] = c_avg['Attendance_Percentage'] - 75.0
        c_avg = c_avg.sort_values(by='Course_Code')
        
        b_cols = ['#93C5FD'] * len(c_avg)
        max_idx = c_avg['Diff'].idxmax()
        b_cols[max_idx] = '#2563EB'  # Highlighted peak bar
        
        fig_ontime = go.Figure()
        fig_ontime.add_trace(go.Bar(
            x=c_avg['Course_Code'],
            y=c_avg['Diff'],
            marker_color=b_cols,
            width=0.38,
            marker_cornerradius=4,
            hovertemplate='<b>%{x}</b>: %{y:+.1f}% vs 75%<extra></extra>'
        ))
        
        # Red Pin Marker & Callout Box exactly as in reference
        fig_ontime.add_annotation(
            x=c_avg.loc[max_idx, 'Course_Code'],
            y=c_avg.loc[max_idx, 'Diff'],
            text="<span style='background:#FFFFFF; border:1px solid #E2E8F0; padding:3px 9px; border-radius:6px; font-size:10px; font-weight:700; color:#0F172A; box-shadow:0 2px 8px rgba(0,0,0,0.06);'><b>400</b> Employees</span>",
            showarrow=True,
            arrowhead=2,
            arrowcolor='#EF4444',
            arrowsize=1,
            ax=0, ay=-28
        )
        
        fig_ontime.add_hline(y=0, line_color='#E2E8F0', line_width=1)
        
        fig_ontime.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            height=200, margin=dict(l=10, r=10, t=30, b=20),
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color='#64748B')),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(size=9, color='#64748B'))
        )
        st.plotly_chart(fig_ontime, width='stretch', config={'displayModeBar': False})
        render_html("</div>")

    with col_overtime:
        render_html("""
<div class="white-card" style="height: 100%;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
<div class="card-header-title" style="margin-bottom:0;">Overtime</div>
<div style="display:flex; gap:6px;">
<span style="background:#2563EB; color:#FFF; font-size:0.7rem; font-weight:700; padding:2px 10px; border-radius:9999px;">Hours</span>
<span style="color:#64748B; font-size:0.7rem; font-weight:600; padding:2px 6px;">Employees</span>
</div>
</div>
""")
        
        # Vertical Bar Chart with Peak Bar in Vibrant Blue
        cond_vals = [16, 16, 24, 17, 17, 17, 17, 17, 17, 17, 17, 17]
        c_names = sorted(df['Course_Code'].unique())
        c_colors = ['#93C5FD'] * len(c_names)
        c_colors[2] = '#2563EB'  # Peak bar (24 classes)
        
        fig_ot = go.Figure()
        fig_ot.add_trace(go.Bar(
            x=c_names,
            y=cond_vals,
            marker_color=c_colors,
            width=0.38,
            marker_cornerradius=4,
            hovertemplate='<b>%{x}</b>: %{y} classes conducted<extra></extra>'
        ))
        
        fig_ot.add_annotation(
            x=c_names[2],
            y=24,
            text="<span style='background:#FFFFFF; border:1px solid #E2E8F0; padding:3px 9px; border-radius:6px; font-size:10px; font-weight:700; color:#0F172A; box-shadow:0 2px 8px rgba(0,0,0,0.06);'><b>40</b> Hours</span>",
            showarrow=True,
            arrowhead=0,
            ax=0, ay=-26
        )
        
        fig_ot.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            height=200, margin=dict(l=10, r=10, t=30, b=20),
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color='#64748B')),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(size=9, color='#64748B'))
        )
        st.plotly_chart(fig_ot, width='stretch', config={'displayModeBar': False})
        render_html("</div>")

    with col_source:
        render_html(f"""
<div class="white-card" style="height: 100%;">
<div class="card-header-title">Attendance Source</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
<div class="inner-stat-box-light">
<div class="inner-stat-label">Device Check-Ins</div>
<div class="inner-stat-val">2,000</div>
</div>
<div class="inner-stat-box-light">
<div class="inner-stat-label">App Check-Ins</div>
<div class="inner-stat-val">2,500</div>
</div>
<div class="inner-stat-box-light">
<div class="inner-stat-label">Active Devices</div>
<div class="inner-stat-val">145</div>
</div>
<div class="inner-stat-box-light">
<div class="inner-stat-label">Inactive Devices</div>
<div class="inner-stat-val" style="color:#EF4444;">5</div>
</div>
</div>
</div>
""")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # ROW 3: EXCEPTIONS & PENDING REQUESTS
    # --------------------------------------------------------------------------
    col_exc, col_req = st.columns([1.9, 1.9])
    
    with col_exc:
        render_html(f"""
<div class="white-card">
<div class="card-header-title">Exceptions</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
<div class="inner-stat-box-light">
<div class="inner-stat-label">Late Coming (&lt; 50% Shortage)</div>
<div class="inner-stat-val" style="color:#EF4444;">{critical_shortage}</div>
</div>
<div class="inner-stat-box-light">
<div class="inner-stat-label">Early Going (50-74% Shortage)</div>
<div class="inner-stat-val" style="color:#F59E0B;">{moderate_shortage}</div>
</div>
</div>
</div>
""")

    with col_req:
        render_html(f"""
<div class="white-card">
<div class="card-header-title">Pending Requests</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
<div class="inner-stat-box-light">
<div class="inner-stat-label">Regularization Requests (Defaulters)</div>
<div class="inner-stat-val" style="color:#2563EB;">{defaulters_students_count}</div>
</div>
<div class="inner-stat-box-light">
<div class="inner-stat-label">Leave Requests (Eligible Students)</div>
<div class="inner-stat-val" style="color:#10B981;">{compliant_students_count}</div>
</div>
</div>
</div>
""")

# ==============================================================================
# VIEW 2: REPORTS / MASTER DATA (Full Table with Filters & CSV Download)
# ==============================================================================
elif nav_selection in ["Reports", "Master Data"]:
    render_html("""
<div class="white-card">
<div class="card-header-title">MBA 2nd Year 3rd sem Master Attendance Reports</div>
""")
    
    c_f1, c_f2, c_btn = st.columns([1.5, 1.5, 1])
    with c_f1:
        st_opts = sorted(list((df['Register_No'] + " - " + df['Student_Name'].str.title()).unique()))
        f_stud = st.multiselect("Filter Student:", options=st_opts, default=[], placeholder="All Students (29)")
    with c_f2:
        c_opts = sorted(list((df['Course_Code'] + " - " + df['Course_Title']).unique()))
        f_course = st.multiselect("Filter Course:", options=c_opts, default=[], placeholder="All Courses (12)")
    with c_btn:
        st.markdown("<div style='height:26px;'></div>", unsafe_allow_html=True)
        csv_exp = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv_exp, file_name="mba_2nd_year_3rd_sem_attendance_report.csv", mime="text/csv", width='stretch')

    f_df = df.copy()
    if f_stud:
        regs = [s.split(" - ")[0] for s in f_stud]
        f_df = f_df[f_df['Register_No'].isin(regs)]
    if f_course:
        cds = [c.split(" - ")[0] for c in f_course]
        f_df = f_df[f_df['Course_Code'].isin(cds)]
        
    st.dataframe(f_df[['S.No', 'Register_No', 'Student_Name', 'Course_Code', 'Course_Title', 'Attendance_Percentage', 'Status']], width='stretch', hide_index=True)
    render_html("</div>")

# ==============================================================================
# VIEW 3: ATTENDANCE (Consecutive Class Recovery Calculator)
# ==============================================================================
elif nav_selection == "Attendance Calculator":
    render_html("""
<div class="white-card">
<div class="card-header-title">MBA 2nd Year 3rd sem Attendance Recovery Calculator</div>
<div style="font-size:0.85rem; color:#64748B; margin-bottom:16px;">
Compute exact upcoming consecutive classes required to surpass the 75% eligibility mark.
</div>
""")
    
    c_c1, c_c2, c_c3 = st.columns([1.5, 2, 1])
    with c_c1:
        s_map = {f"{r['Register_No']} - {r['Student_Name']}": r['Register_No'] for _, r in df[['Register_No', 'Student_Name']].drop_duplicates().iterrows()}
        c_student = st.selectbox("Select Student:", options=list(s_map.keys()), index=0)
        c_reg = s_map[c_student]
        c_st_df = df[df['Register_No'] == c_reg].copy().sort_values(by='Course_Code')
    
    with c_c2:
        c_crs_map = {f"{r['Course_Code']} - {r['Course_Title']} ({r['Attendance_Percentage']:.1f}%)": r['Course_Code'] for _, r in c_st_df.iterrows()}
        c_course_lbl = st.selectbox("Select Enrolled Subject:", options=list(c_crs_map.keys()), index=0)
        c_code = c_crs_map[c_course_lbl]
        
    with c_c3:
        target_pct = st.number_input("Target Benchmark (%):", min_value=50.0, max_value=99.0, value=float(threshold), step=1.0)

    s_row = c_st_df[c_st_df['Course_Code'] == c_code].iloc[0]
    t_c = int(s_row['Classes_Conducted'])
    t_a = int(s_row['Classes_Attended'])
    t_m = t_c - t_a
    c_p = s_row['Attendance_Percentage']
    
    need_cls, safe_bunk, _ = calculate_attendance_needs(t_c, t_a, target_pct)
    
    c_res_box, c_res_curve = st.columns([1.2, 1.8])
    with c_res_box:
        if c_p < target_pct:
            new_tot = t_c + need_cls
            new_att = t_a + need_cls
            new_p = (new_att / new_tot) * 100.0
            render_html(f"""
<div class="inner-stat-box-light" style="border-left:4px solid #EF4444; background:#FEF2F2; padding:18px;">
<div style="font-size:0.75rem; font-weight:800; color:#EF4444; letter-spacing:0.8px;">ATTENDANCE SHORTAGE</div>
<div style="font-size:2rem; font-weight:800; color:#0F172A; margin:6px 0;">Attend {need_cls} Classes</div>
<div style="font-size:0.86rem; color:#475569; line-height:1.45; margin-bottom:12px;">
Must attend <b>{need_cls} consecutive upcoming classes</b> to elevate attendance from <b>{c_p:.2f}%</b> to <b>{new_p:.2f}%</b> (&ge; {target_pct:.0f}%).
</div>
<div style="font-size:0.78rem; color:#64748B; display:grid; grid-template-columns:1fr 1fr; gap:6px;">
<div>Conducted: <b>{t_c}</b></div>
<div>Attended: <b>{t_a}</b></div>
<div>Missed: <b>{t_m}</b></div>
<div>New Total: <b>{new_tot}</b></div>
</div>
</div>
""")
        else:
            render_html(f"""
<div class="inner-stat-box-light" style="border-left:4px solid #10B981; background:#F0FDF4; padding:18px;">
<div style="font-size:0.75rem; font-weight:800; color:#10B981; letter-spacing:0.8px;">ELIGIBILITY MET</div>
<div style="font-size:2rem; font-weight:800; color:#0F172A; margin:6px 0;">0 Classes Needed</div>
<div style="font-size:0.86rem; color:#475569; line-height:1.45; margin-bottom:12px;">
Current attendance is <b>{c_p:.2f}%</b>, meeting the <b>{target_pct:.0f}%</b> requirement.
Safe Miss Buffer: <b>{safe_bunk} upcoming classes</b>.
</div>
</div>
""")

    with c_res_curve:
        sim_max = max(12, need_cls + 6)
        x_vals = list(range(0, sim_max + 1))
        y_vals = [((t_a + x) / (t_c + x)) * 100.0 for x in x_vals]
        
        fig_curve = go.Figure()
        fig_curve.add_hline(y=target_pct, line_dash="dash", line_color="#EF4444", annotation_text=f"Target {target_pct:.0f}%")
        fig_curve.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='lines+markers',
            line=dict(color='#2563EB', width=2.5), marker=dict(size=6, color='#2563EB'),
            hovertemplate='Attend +<b>%{x}</b> classes: <b>%{y:.2f}%</b><extra></extra>'
        ))
        if need_cls > 0 and need_cls <= sim_max:
            fig_curve.add_trace(go.Scatter(
                x=[need_cls], y=[y_vals[need_cls]], mode='markers', name='Milestone',
                marker=dict(size=12, color='#10B981', symbol='star')
            ))
        fig_curve.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=240,
            xaxis=dict(title='Consecutive Upcoming Classes Attended', showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#64748B')),
            yaxis=dict(title='Projected %', showgrid=True, gridcolor='#F1F5F9', ticksuffix='%', tickfont=dict(color='#64748B')),
            margin=dict(l=10, r=10, t=30, b=10), showlegend=False
        )
        st.plotly_chart(fig_curve, width='stretch', config={'displayModeBar': False})
        
    render_html("</div>")

# ==============================================================================
# VIEW 4: DEFAULTERS & LEAVES
# ==============================================================================
else:
    render_html(f"""
<div class="white-card">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
<div class="card-header-title" style="margin-bottom:0;">MBA 2nd Year 3rd sem Defaulters &amp; Leave Registry</div>
</div>
""")
    
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        st.write(f"Total **{defaulters_students_count}** MBA students requiring regularization for attendance under **{threshold}%**.")
    with col_d2:
        exp_csv = df[df['Attendance_Percentage'] < threshold].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Defaulters CSV", data=exp_csv, file_name=f"mba_defaulters_below_{threshold}pct.csv", mime="text/csv", width='stretch')
        
    def_disp = defaulters_df.copy()
    def_disp['Lowest_Percentage'] = def_disp['lowest_pct'].apply(lambda x: f"{x:.2f}%")
    def_disp['Average_Percentage'] = def_disp['avg_pct'].apply(lambda x: f"{x:.2f}%")
    def_disp.rename(columns={
        'Register_No': 'Register No',
        'Student_Name': 'Student Name',
        'shortages': 'Deficit Subjects (out of 6)',
        'courses': 'Deficit Course Codes',
        'Lowest_Percentage': 'Lowest %',
        'Average_Percentage': 'Defaulter Courses Avg %'
    }, inplace=True)
    
    st.dataframe(def_disp[['Register No', 'Student Name', 'Deficit Subjects (out of 6)', 'Deficit Course Codes', 'Lowest %', 'Defaulter Courses Avg %']], width='stretch', hide_index=True)
    render_html("</div>")
