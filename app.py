import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(
    page_title="Riko — Finance Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

RIKO_SVG = """
<svg width="80" height="80" viewBox="270 55 150 260" xmlns="http://www.w3.org/2000/svg" style="shape-rendering:crispEdges;">
<ellipse cx="340" cy="290" rx="90" ry="18" fill="#7c3aed" opacity="0.18"/>
<rect x="290" y="170" width="100" height="90" rx="8" fill="#1e1145"/>
<rect x="294" y="174" width="92" height="82" rx="6" fill="#2d1a6e"/>
<rect x="305" y="185" width="70" height="28" rx="4" fill="#0d0726"/>
<rect x="308" y="188" width="64" height="22" rx="3" fill="#0a0520"/>
<rect x="315" y="200" width="6" height="7" rx="1" fill="#7c3aed"/>
<rect x="324" y="196" width="6" height="11" rx="1" fill="#a78bfa"/>
<rect x="333" y="192" width="6" height="15" rx="1" fill="#c4b5fd"/>
<rect x="342" y="198" width="6" height="9" rx="1" fill="#a78bfa"/>
<rect x="351" y="194" width="6" height="13" rx="1" fill="#7c3aed"/>
<rect x="360" y="197" width="6" height="10" rx="1" fill="#c4b5fd"/>
<circle cx="310" cy="228" r="5" fill="#7c3aed"/>
<circle cx="310" cy="228" r="3" fill="#a78bfa"/>
<rect x="320" y="223" width="18" height="9" rx="4" fill="#4f46e5"/>
<rect x="344" y="223" width="12" height="9" rx="4" fill="#6366f1"/>
<rect x="362" y="223" width="12" height="9" rx="4" fill="#7c3aed"/>
<rect x="308" y="258" width="28" height="24" rx="4" fill="#1e1145"/>
<rect x="344" y="258" width="28" height="24" rx="4" fill="#1e1145"/>
<rect x="304" y="278" width="34" height="12" rx="5" fill="#2d1a6e"/>
<rect x="342" y="278" width="34" height="12" rx="5" fill="#2d1a6e"/>
<rect x="308" y="280" width="20" height="4" rx="2" fill="#4f46e5"/>
<rect x="346" y="280" width="20" height="4" rx="2" fill="#4f46e5"/>
<rect x="264" y="175" width="28" height="16" rx="6" fill="#2d1a6e"/>
<rect x="252" y="172" width="16" height="22" rx="7" fill="#1e1145"/>
<circle cx="244" cy="196" r="12" fill="#2d1a6e"/>
<circle cx="244" cy="196" r="9" fill="#fbbf24"/>
<text x="244" y="200" text-anchor="middle" font-size="11" font-weight="700" fill="#92400e">&#8377;</text>
<rect x="388" y="175" width="28" height="16" rx="6" fill="#2d1a6e"/>
<rect x="404" y="172" width="16" height="22" rx="7" fill="#1e1145"/>
<circle cx="418" cy="166" r="11" fill="#2d1a6e"/>
<rect x="415" y="150" width="7" height="16" rx="3" fill="#c4b5fd"/>
<rect x="413" y="158" width="5" height="12" rx="3" fill="#c4b5fd"/>
<rect x="421" y="158" width="5" height="12" rx="3" fill="#c4b5fd"/>
<rect x="294" y="90" width="92" height="82" rx="12" fill="#1e1145"/>
<rect x="298" y="94" width="84" height="74" rx="10" fill="#2d1a6e"/>
<rect x="337" y="70" width="6" height="22" rx="3" fill="#4f46e5"/>
<circle cx="340" cy="64" r="9" fill="#7c3aed"/>
<circle cx="340" cy="64" r="6" fill="#a78bfa"/>
<circle cx="340" cy="64" r="3" fill="#ffffff" opacity="0.9"/>
<rect x="286" y="118" width="10" height="22" rx="5" fill="#1e1145"/>
<rect x="384" y="118" width="10" height="22" rx="5" fill="#1e1145"/>
<rect x="287" y="122" width="8" height="14" rx="4" fill="#4f46e5"/>
<rect x="385" y="122" width="8" height="14" rx="4" fill="#4f46e5"/>
<rect x="308" y="106" width="64" height="50" rx="8" fill="#0a0520"/>
<rect x="311" y="109" width="58" height="44" rx="6" fill="#0d0726"/>
<path d="M322 128 Q330 118 338 128" stroke="#a78bfa" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<circle cx="325" cy="124" r="2" fill="#c4b5fd" opacity="0.8"/>
<path d="M343 124 Q351 124 359 124" stroke="#a78bfa" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<path d="M341 121 Q351 129 361 121" stroke="#a78bfa" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.5"/>
<circle cx="317" cy="140" r="7" fill="#f87171" opacity="0.3"/>
<circle cx="363" cy="140" r="7" fill="#f87171" opacity="0.3"/>
<path d="M324 140 Q340 154 356 140" stroke="#a78bfa" stroke-width="3" fill="none" stroke-linecap="round"/>
<circle cx="265" cy="150" r="2.5" fill="#fbbf24" opacity="0.8"/>
</svg>
"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg,
        #0a0015 0%, #0d0a2e 20%, #0a0a2a 40%,
        #120a30 60%, #0d0520 80%, #050010 100%
    ) !important;
    background-attachment: fixed !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

/* Hide sidebar entirely */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139,92,246,0.25) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.5rem !important;
}
[data-testid="stMetricLabel"] {
    color: #a78bfa !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid rgba(139,92,246,0.2) !important;
    overflow: hidden;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(139,92,246,0.05) !important;
    border: 2px dashed rgba(139,92,246,0.4) !important;
    border-radius: 14px !important;
}

/* Alerts */
.stAlert {
    border-radius: 12px !important;
    background: rgba(139,92,246,0.1) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
}
.stAlert p { color: #c4b5fd !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #6d5fa6 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(139,92,246,0.25) !important;
    color: #c4b5fd !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SAMPLE_CSV = """date,amount,category,merchant,hour
2024-01-01,450,Food,Swiggy,13
2024-01-02,1200,Shopping,Amazon,22
2024-01-03,300,Transport,Uber,9
2024-01-04,800,Food,Zomato,23
2024-01-05,2500,Shopping,Myntra,21
2024-01-06,150,Transport,Rapido,8
2024-01-07,600,Entertainment,BookMyShow,19
2024-01-08,950,Food,Swiggy,22
2024-01-09,3200,Shopping,Amazon,23
2024-01-10,200,Transport,Uber,7
2024-01-11,750,Food,Zomato,20
2024-01-12,1800,Shopping,Flipkart,21
2024-01-13,100,Transport,Rapido,9
2024-01-14,500,Entertainment,Netflix,18
2024-01-15,420,Food,Swiggy,12
2024-01-16,2100,Shopping,Amazon,22
2024-01-17,350,Food,McDonald's,13
2024-01-18,680,Entertainment,PVR,20
2024-01-19,900,Food,Zomato,23
2024-01-20,1500,Shopping,Myntra,21
2024-01-21,250,Transport,Uber,8
2024-01-22,1100,Food,Swiggy,22
2024-01-23,400,Entertainment,Spotify,17
2024-01-24,750,Shopping,Flipkart,20
2024-01-25,200,Transport,Rapido,7
2024-01-26,850,Food,Zomato,21
2024-01-27,2800,Shopping,Amazon,23
2024-01-28,300,Transport,Uber,9
2024-01-29,650,Entertainment,BookMyShow,19
2024-01-30,1200,Food,Swiggy,22"""

# ── TOP NAV BAR ───────────────────────────────────────
col_logo, col_title, col_upload, col_source = st.columns([0.8, 2.5, 2, 1.5])

with col_logo:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:10px; padding-top:0.6rem;'>
            {RIKO_SVG}
            <div>
                <div style='font-size:1.2rem; font-weight:800;
                            background:linear-gradient(135deg,#a78bfa,#7c3aed);
                            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                            line-height:1;'>Riko</div>
                <div style='font-size:0.62rem; color:#7c3aed; letter-spacing:0.1em;
                            text-transform:uppercase;'>Finance AI</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown("""
        <div style='padding-top:1.4rem;'>
            <span style='font-size:1.3rem; font-weight:700; color:#ffffff;'>
                Personal Finance Intelligence
            </span>
            <br>
            <span style='font-size:0.78rem; color:#6d5fa6;'>
                Spending insights · Behavioral patterns · Smart recommendations
            </span>
        </div>
    """, unsafe_allow_html=True)

with col_upload:
    st.markdown("<div style='padding-top:0.8rem;'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your CSV",
        type=["csv"],
        label_visibility="collapsed",
        help="Columns: date, amount, category, merchant, hour"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_source:
    st.markdown("<div style='padding-top:0.9rem;'>", unsafe_allow_html=True)
    use_sample = st.toggle("Sample data", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <hr style='border:none; border-top:1px solid rgba(139,92,246,0.2); margin:0.5rem 0 1.5rem 0;'>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────
if use_sample or uploaded_file is None:
    df = pd.read_csv(StringIO(SAMPLE_CSV))
    if use_sample:
        st.markdown("""
            <div style='background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);
                        border-radius:10px;padding:0.6rem 1rem;margin-bottom:1.2rem;
                        font-size:0.82rem;color:#a78bfa;'>
                ✨ Showing <strong style='color:#c4b5fd;'>sample data</strong> —
                30 transactions. Toggle off "Sample data" and upload your own CSV to analyse it.
            </div>
        """, unsafe_allow_html=True)
else:
    df = pd.read_csv(uploaded_file)

# ── CLEAN ─────────────────────────────────────────────
df.columns = df.columns.str.lower().str.strip()
df.drop_duplicates(inplace=True)
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
if 'hour' in df.columns:
    def spending_time(h):
        if h < 12: return "Morning"
        elif h < 17: return "Afternoon"
        elif h < 21: return "Evening"
        return "Night"
    df['time_period'] = df['hour'].apply(spending_time)

total_spending = df['amount'].sum()
avg_spending   = df['amount'].mean()
highest        = df['amount'].max()
count          = len(df)

CHART = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#a78bfa', family='Inter'),
    title_font=dict(color='#ffffff', size=15, family='Inter'),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a78bfa')),
    xaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)'),
    yaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)'),
    margin=dict(l=20, r=20, t=40, b=20),
)
GC = ['#7c3aed','#6366f1','#a78bfa','#4f46e5','#8b5cf6','#c4b5fd','#312e81','#5b21b6']

def label(txt):
    st.markdown(f"""
        <div style='font-size:0.72rem;color:#7c3aed;font-weight:600;
                    text-transform:uppercase;letter-spacing:0.1em;
                    margin-bottom:1rem;margin-top:0.5rem;'>✦ {txt}</div>
    """, unsafe_allow_html=True)

# ── TABS (navigation) ─────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Overview",
    "📈  Analytics",
    "🧠  Behavior",
    "💡  Recommendations"
])

# ── OVERVIEW ──────────────────────────────────────────
with tab1:
    label("Financial Snapshot")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("💸 Total Spending",      f"₹{round(total_spending):,}")
    c2.metric("📈 Avg per Transaction", f"₹{round(avg_spending):,}")
    c3.metric("🔥 Highest Expense",     f"₹{round(highest):,}")
    c4.metric("🧾 Total Transactions",  count)
    st.markdown("<br>", unsafe_allow_html=True)
    label("Transaction Log")
    st.dataframe(df, use_container_width=True, height=380)

# ── ANALYTICS ─────────────────────────────────────────
with tab2:
    label("Spending Analytics")
    c1, c2 = st.columns(2)
    if 'category' in df.columns:
        cat = df.groupby('category')['amount'].sum().reset_index()
        f1 = px.bar(cat, x='category', y='amount', title="By Category",
                    color='amount',
                    color_continuous_scale=[[0,'#312e81'],[0.5,'#6366f1'],[1,'#a78bfa']])
        f1.update_layout(**CHART, coloraxis_showscale=False)
        f1.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        c1.plotly_chart(f1, use_container_width=True)
    if 'merchant' in df.columns:
        m = (df.groupby('merchant')['amount'].sum()
             .reset_index().sort_values('amount', ascending=True).tail(8))
        f2 = px.bar(m, x='amount', y='merchant', orientation='h', title="Top Merchants",
                    color='amount',
                    color_continuous_scale=[[0,'#4f46e5'],[0.5,'#7c3aed'],[1,'#c4b5fd']])
        f2.update_layout(**CHART, coloraxis_showscale=False)
        f2.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        c2.plotly_chart(f2, use_container_width=True)
    if 'date' in df.columns:
        daily = df.groupby('date')['amount'].sum().reset_index()
        f3 = go.Figure()
        f3.add_trace(go.Scatter(
            x=daily['date'], y=daily['amount'], mode='lines+markers',
            line=dict(color='#a78bfa', width=2.5),
            marker=dict(color='#7c3aed', size=6, line=dict(color='#c4b5fd', width=1.5)),
            fill='tozeroy', fillcolor='rgba(139,92,246,0.08)'
        ))
        f3.update_layout(**CHART, title_text="Daily Spending Trend", showlegend=False)
        st.plotly_chart(f3, use_container_width=True)
    if 'category' in df.columns:
        f4 = px.pie(df.groupby('category')['amount'].sum().reset_index(),
                    values='amount', names='category', title="Category Breakdown",
                    color_discrete_sequence=GC, hole=0.45)
        f4.update_layout(**CHART)
        f4.update_traces(textfont=dict(color='white'),
                         marker=dict(line=dict(color='rgba(10,5,30,0.8)', width=2)))
        st.plotly_chart(f4, use_container_width=True)

# ── BEHAVIOR ──────────────────────────────────────────
with tab3:
    label("Behavioral Analysis")
    if 'hour' in df.columns:
        df['impulsive'] = (df['hour'] >= 22) | (df['amount'] > 700)
        ic = int(df['impulsive'].sum())
        nc = count - ic
        c1,c2,c3 = st.columns(3)
        c1.metric("⚠️ Impulsive Purchases", ic)
        c2.metric("✅ Normal Purchases", nc)
        c3.metric("📊 Impulsive Rate", f"{round(ic/count*100)}%")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        f4 = go.Figure(go.Pie(
            labels=['Impulsive','Normal'], values=[ic, nc], hole=0.5,
            marker=dict(colors=['#f87171','#6366f1'],
                        line=dict(color='rgba(10,5,30,0.8)', width=2)),
            textfont=dict(color='white')
        ))
        f4.update_layout(**CHART, title_text="Behaviour Breakdown")
        col1.plotly_chart(f4, use_container_width=True)
        if 'time_period' in df.columns:
            td = df.groupby('time_period')['amount'].sum().reset_index()
            f5 = px.bar(td, x='time_period', y='amount',
                        title="Spending by Time of Day", color='time_period',
                        color_discrete_map={'Morning':'#fbbf24','Afternoon':'#6366f1',
                                            'Evening':'#34d399','Night':'#f87171'})
            f5.update_layout(**CHART, showlegend=False)
            col2.plotly_chart(f5, use_container_width=True)
    else:
        st.info("Add an 'hour' column (0–23) to unlock behavioral insights.")

# ── RECOMMENDATIONS ───────────────────────────────────
with tab4:
    label("Smart Recommendations")
    recs = []
    if avg_spending > 700:
        recs.append(("💡","High Average Spend",
            f"Your average transaction is ₹{round(avg_spending):,}. Consider a monthly cap.",
            "#7c3aed"))
    if 'merchant' in df.columns:
        top_m = df.groupby('merchant')['amount'].sum().idxmax()
        top_a = df.groupby('merchant')['amount'].sum().max()
        recs.append(("🛍️",f"Top Merchant: {top_m}",
            f"₹{round(top_a):,} spent here. Worth monitoring closely.", "#6366f1"))
    if 'hour' in df.columns:
        night = df[df['hour'] >= 22]['amount'].sum()
        if night > 0:
            recs.append(("🌙","Late Night Spending",
                f"₹{round(night):,} spent after 10pm. Try a spending cut-off.", "#8b5cf6"))
    if count > 20:
        recs.append(("📊","Transaction Volume",
            f"{count} transactions logged. Weekly reviews help catch patterns early.",
            "#4f46e5"))
    if not recs:
        st.success("🎉 Healthy spending detected! Keep it up.")
    else:
        for icon, title, text, color in recs:
            st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03);
                            border:1px solid rgba(139,92,246,0.2);
                            border-left:4px solid {color};
                            border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;'>
                    <div style='font-weight:700;color:#ffffff;
                                margin-bottom:0.4rem;font-size:0.95rem;'>{icon} {title}</div>
                    <div style='color:#9ca3af;font-size:0.87rem;line-height:1.6;'>{text}</div>
                </div>
            """, unsafe_allow_html=True)
