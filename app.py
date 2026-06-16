import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

st.set_page_config(
    page_title="Riko — Finance Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,
        #0a0015 0%, #0d0a2e 20%, #0a0a2a 40%,
        #120a30 60%, #0d0520 80%, #050010 100%
    ) !important;
    background-attachment: fixed !important;
}
/* Force sidebar always open — hide collapse button */
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
[data-testid="stSidebarContent"] {
    transform: none !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: 0 !important;
    transform: translateX(0) !important;
    width: 280px !important;
    min-width: 280px !important;
    visibility: visible !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

[data-testid="stSidebar"] {
    background: rgba(15, 8, 40, 0.97) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.25) !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #c4b5fd !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: #a78bfa !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(139, 92, 246, 0.15) !important;
}

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.5rem !important;
    backdrop-filter: blur(10px);
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

[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    overflow: hidden;
}

[data-testid="stFileUploader"] {
    background: rgba(139, 92, 246, 0.05) !important;
    border: 2px dashed rgba(139, 92, 246, 0.4) !important;
    border-radius: 14px !important;
}

.stAlert {
    border-radius: 12px !important;
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
}

.stAlert p { color: #c4b5fd !important; }

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    font-size: 0.88rem !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
    transform: translateY(-1px);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SAMPLE DATA ───────────────────────────────────────
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

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding-bottom: 1.5rem;'>
            <div style='font-size: 2.8rem;
                        filter: drop-shadow(0 0 12px rgba(139,92,246,0.8));'>💰</div>
            <div style='font-size: 1.5rem; font-weight: 800;
                        background: linear-gradient(135deg, #a78bfa, #7c3aed);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        margin-top: 0.3rem;'>Riko</div>
            <div style='font-size: 0.72rem; color: #7c3aed; letter-spacing: 0.12em;
                        text-transform: uppercase; margin-top: 2px;'>Finance Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    selected = st.radio(
        "Navigation",
        ["📊 Overview", "📈 Analytics", "🧠 Behavior", "💡 Recommendations"],
        label_visibility="collapsed"
    )

    st.markdown("""
        <hr style='border:none; border-top:1px solid rgba(139,92,246,0.2); margin: 1rem 0;'>
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.6rem;'>
            Data Source
        </div>
    """, unsafe_allow_html=True)

    data_source = st.radio(
        "data_source",
        ["✨ Use sample data", "📁 Upload my CSV"],
        label_visibility="collapsed"
    )

    uploaded_file = None
    if data_source == "📁 Upload my CSV":
        uploaded_file = st.file_uploader(
            "Upload CSV",
            type=["csv"],
            help="Columns: date, amount, category, merchant, hour"
        )

    st.markdown("""
        <div style='margin-top: 1rem; padding: 0.9rem 1rem;
                    background: rgba(139,92,246,0.08);
                    border-radius: 10px; border: 1px solid rgba(139,92,246,0.2);'>
            <div style='font-size: 0.72rem; color: #a78bfa; font-weight: 600;
                        text-transform: uppercase; letter-spacing: 0.08em;'>
                📋 Expected columns
            </div>
            <div style='font-size: 0.75rem; color: #6d5fa6;
                        margin-top: 6px; line-height: 1.6;'>
                date · amount · category<br>merchant · hour
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────
st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <div style='font-size: 0.72rem; color: #7c3aed; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem;'>
            ✦ AI-POWERED DASHBOARD
        </div>
        <h1 style='font-size: 2.2rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 60%, #7c3aed 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Personal Finance Intelligence
        </h1>
        <p style='color: #6d5fa6; margin: 0.4rem 0 0 0; font-size: 0.92rem;'>
            Spending insights · Behavioral patterns · Smart recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────
if data_source == "✨ Use sample data":
    df = pd.read_csv(StringIO(SAMPLE_CSV))
    st.markdown("""
        <div style='background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.3);
                    border-radius: 10px; padding: 0.7rem 1rem; margin-bottom: 1.5rem;
                    font-size: 0.82rem; color: #a78bfa;'>
            ✨ Showing <strong style='color:#c4b5fd;'>sample data</strong> —
            30 transactions across Food, Shopping, Transport & Entertainment.
            Switch to "Upload my CSV" in the sidebar to use your own data.
        </div>
    """, unsafe_allow_html=True)
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    col1, col2, col3 = st.columns(3)
    for col, (icon, title, desc) in zip([col1, col2, col3], [
        ("📂", "Upload CSV", "Bank statements, UPI exports,<br>GPay, PhonePe, Paytm"),
        ("🧠", "Get Insights", "Spending patterns, behavioral<br>analysis, risk detection"),
        ("💡", "Take Action", "Personalised recommendations<br>to improve your finances"),
    ]):
        with col:
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03);
                            border: 1px solid rgba(139,92,246,0.2);
                            border-radius: 18px; padding: 1.8rem 1.5rem;
                            text-align: center;'>
                    <div style='font-size:2.2rem; margin-bottom:0.8rem;'>{icon}</div>
                    <div style='font-weight:700; color:#ffffff; margin-bottom:0.5rem;'>{title}</div>
                    <div style='font-size:0.78rem; color:#6d5fa6; line-height:1.5;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Choose **Use sample data** or upload your own CSV from the sidebar.")
    st.stop()

# ── CLEAN DATA ────────────────────────────────────────
df.columns = df.columns.str.lower().str.strip()
df.drop_duplicates(inplace=True)

if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

if 'hour' in df.columns:
    def spending_time(hour):
        if hour < 12: return "Morning"
        elif hour < 17: return "Afternoon"
        elif hour < 21: return "Evening"
        return "Night"
    df['time_period'] = df['hour'].apply(spending_time)

total_spending = df['amount'].sum()
avg_spending = df['amount'].mean()
highest_expense = df['amount'].max()
transaction_count = len(df)

# ── CHART THEME ───────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#a78bfa', family='Inter'),
    title_font=dict(color='#ffffff', size=15, family='Inter'),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a78bfa')),
    xaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)', showgrid=True),
    yaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)', showgrid=True),
    margin=dict(l=20, r=20, t=40, b=20),
)

GALAXY_COLORS = ['#7c3aed','#6366f1','#a78bfa','#4f46e5',
                 '#8b5cf6','#c4b5fd','#312e81','#5b21b6']

def section_label(text):
    st.markdown(f"""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:1rem; margin-top:0.5rem;'>
            ✦ {text}
        </div>
    """, unsafe_allow_html=True)

# ── PAGE: OVERVIEW ────────────────────────────────────
if selected == "📊 Overview":
    section_label("Financial Snapshot")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💸 Total Spending",     f"₹{round(total_spending):,}")
    c2.metric("📈 Avg per Transaction",f"₹{round(avg_spending):,}")
    c3.metric("🔥 Highest Expense",    f"₹{round(highest_expense):,}")
    c4.metric("🧾 Total Transactions", transaction_count)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Transaction Log")
    st.dataframe(df, use_container_width=True, height=380)

# ── PAGE: ANALYTICS ───────────────────────────────────
elif selected == "📈 Analytics":
    section_label("Spending Analytics")
    col1, col2 = st.columns(2)

    if 'category' in df.columns:
        cat = df.groupby('category')['amount'].sum().reset_index()
        fig1 = px.bar(cat, x='category', y='amount', title="By Category",
                      color='amount',
                      color_continuous_scale=[[0,'#312e81'],[0.5,'#6366f1'],[1,'#a78bfa']])
        fig1.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
        fig1.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        col1.plotly_chart(fig1, use_container_width=True)

    if 'merchant' in df.columns:
        merch = (df.groupby('merchant')['amount'].sum()
                 .reset_index().sort_values('amount', ascending=True).tail(8))
        fig2 = px.bar(merch, x='amount', y='merchant', orientation='h',
                      title="Top Merchants",
                      color='amount',
                      color_continuous_scale=[[0,'#4f46e5'],[0.5,'#7c3aed'],[1,'#c4b5fd']])
        fig2.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
        fig2.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        col2.plotly_chart(fig2, use_container_width=True)

    if 'date' in df.columns:
        daily = df.groupby('date')['amount'].sum().reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=daily['date'], y=daily['amount'],
            mode='lines+markers',
            line=dict(color='#a78bfa', width=2.5),
            marker=dict(color='#7c3aed', size=6,
                        line=dict(color='#c4b5fd', width=1.5)),
            fill='tozeroy',
            fillcolor='rgba(139,92,246,0.08)',
        ))
        fig3.update_layout(**CHART_LAYOUT, title_text="Daily Spending Trend",
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    if 'category' in df.columns:
        fig4 = px.pie(
            df.groupby('category')['amount'].sum().reset_index(),
            values='amount', names='category',
            title="Category Breakdown",
            color_discrete_sequence=GALAXY_COLORS, hole=0.45
        )
        fig4.update_layout(**CHART_LAYOUT)
        fig4.update_traces(
            textfont=dict(color='white'),
            marker=dict(line=dict(color='rgba(10,5,30,0.8)', width=2))
        )
        st.plotly_chart(fig4, use_container_width=True)

# ── PAGE: BEHAVIOR ────────────────────────────────────
elif selected == "🧠 Behavior":
    section_label("Behavioral Analysis")

    if 'hour' in df.columns:
        df['impulsive'] = (df['hour'] >= 22) | (df['amount'] > 700)
        impulsive_count = int(df['impulsive'].sum())
        normal_count = transaction_count - impulsive_count

        c1, c2, c3 = st.columns(3)
        c1.metric("⚠️ Impulsive Purchases", impulsive_count)
        c2.metric("✅ Normal Purchases", normal_count)
        c3.metric("📊 Impulsive Rate",
                  f"{round(impulsive_count / transaction_count * 100)}%")

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        fig4 = go.Figure(go.Pie(
            labels=['Impulsive', 'Normal'],
            values=[impulsive_count, normal_count],
            hole=0.5,
            marker=dict(colors=['#f87171','#6366f1'],
                        line=dict(color='rgba(10,5,30,0.8)', width=2)),
            textfont=dict(color='white')
        ))
        fig4.update_layout(**CHART_LAYOUT, title_text="Behaviour Breakdown")
        col1.plotly_chart(fig4, use_container_width=True)

        if 'time_period' in df.columns:
            time_data = df.groupby('time_period')['amount'].sum().reset_index()
            color_map = {'Morning':'#fbbf24','Afternoon':'#6366f1',
                         'Evening':'#34d399','Night':'#f87171'}
            fig5 = px.bar(time_data, x='time_period', y='amount',
                          title="Spending by Time of Day",
                          color='time_period', color_discrete_map=color_map)
            fig5.update_layout(**CHART_LAYOUT, showlegend=False)
            col2.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Add an 'hour' column (0–23) to unlock behavioral insights.")

# ── PAGE: RECOMMENDATIONS ─────────────────────────────
elif selected == "💡 Recommendations":
    section_label("Smart Recommendations")

    recs = []

    if avg_spending > 700:
        recs.append(("💡", "High Average Spend",
            f"Your average transaction is ₹{round(avg_spending):,}. "
            "Consider setting a monthly cap.", "#7c3aed"))

    if 'merchant' in df.columns:
        top_m = df.groupby('merchant')['amount'].sum().idxmax()
        top_a = df.groupby('merchant')['amount'].sum().max()
        recs.append(("🛍️", f"Top Merchant: {top_m}",
            f"₹{round(top_a):,} spent here. Worth monitoring closely.", "#6366f1"))

    if 'hour' in df.columns:
        night = df[df['hour'] >= 22]['amount'].sum()
        if night > 0:
            recs.append(("🌙", "Late Night Spending",
                f"₹{round(night):,} spent after 10pm — often impulsive. "
                "Try a spending cut-off.", "#8b5cf6"))

    if transaction_count > 20:
        recs.append(("📊", "Transaction Volume",
            f"{transaction_count} transactions logged. "
            "Weekly budget reviews help catch patterns early.", "#4f46e5"))

    if not recs:
        st.success("🎉 Healthy spending detected! Keep it up.")
    else:
        for icon, title, text, color in recs:
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03);
                            border: 1px solid rgba(139,92,246,0.2);
                            border-left: 4px solid {color};
                            border-radius: 14px; padding: 1.2rem 1.5rem;
                            margin-bottom: 1rem;'>
                    <div style='font-weight:700; color:#ffffff;
                                margin-bottom:0.4rem; font-size:0.95rem;'>
                        {icon} {title}
                    </div>
                    <div style='color:#9ca3af; font-size:0.87rem; line-height:1.6;'>
                        {text}
                    </div>
                </div>
            """, unsafe_allow_html=True)
