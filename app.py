import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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

/* ── GALAXY BACKGROUND ── */
.stApp {
    background: linear-gradient(135deg,
        #0a0015 0%,
        #0d0a2e 20%,
        #0a0a2a 40%,
        #120a30 60%,
        #0d0520 80%,
        #050010 100%
    ) !important;
    background-attachment: fixed !important;
}

/* Stars effect overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 70%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 20%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 50%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 80%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 10% 60%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 40%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 50% 90%, rgba(200,180,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 30% 10%, rgba(180,200,255,0.5) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── BLOCK CONTAINER ── */
.block-container {
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    position: relative;
    z-index: 1;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(15, 8, 40, 0.95) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #c4b5fd !important;
}

/* Radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: #a78bfa !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    transition: all 0.2s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(139, 92, 246, 0.15) !important;
}

/* ── METRIC CARDS ── */
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

[data-testid="stMetricDelta"] {
    color: #34d399 !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    overflow: hidden;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(139, 92, 246, 0.05) !important;
    border: 2px dashed rgba(139, 92, 246, 0.4) !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] label {
    color: #c4b5fd !important;
}

/* ── INFO BOX ── */
.stAlert {
    border-radius: 12px !important;
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    color: #c4b5fd !important;
}

.stAlert p {
    color: #c4b5fd !important;
}

/* ── SUCCESS BOX ── */
.element-container .stAlert[data-baseweb="notification"] {
    background: rgba(52, 211, 153, 0.1) !important;
    border: 1px solid rgba(52, 211, 153, 0.3) !important;
}

/* ── HIDE STREAMLIT UI ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding-bottom: 1.5rem;'>
            <div style='font-size: 2.8rem; filter: drop-shadow(0 0 12px rgba(139,92,246,0.8));'>💰</div>
            <div style='font-size: 1.5rem; font-weight: 800; color: #ffffff;
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
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your CSV",
        type=["csv"],
        help="Upload a transaction CSV with columns: date, amount, category, merchant, hour"
    )

    st.markdown("""
        <div style='margin-top: 1rem; padding: 0.9rem 1rem;
                    background: rgba(139,92,246,0.08);
                    border-radius: 10px; border: 1px solid rgba(139,92,246,0.2);'>
            <div style='font-size: 0.72rem; color: #a78bfa; font-weight: 600;
                        text-transform: uppercase; letter-spacing: 0.08em;'>
                📋 Sample columns
            </div>
            <div style='font-size: 0.75rem; color: #6d5fa6; margin-top: 6px; line-height: 1.6;'>
                date · amount · category<br>merchant · hour
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────
st.markdown("""
    <div style='margin-bottom: 2rem; position: relative;'>
        <div style='font-size: 0.72rem; color: #7c3aed; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem;'>
            ✦ AI-POWERED DASHBOARD
        </div>
        <h1 style='font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 0;
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 60%, #7c3aed 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Personal Finance Intelligence
        </h1>
        <p style='color: #6d5fa6; margin: 0.4rem 0 0 0; font-size: 0.92rem;'>
            Upload your transaction data → get spending insights, behavioral patterns, and smart recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# ── NO FILE STATE ─────────────────────────────────────
if uploaded_file is None:
    col1, col2, col3 = st.columns(3)
    cards = [
        ("📂", "Upload CSV", "Bank statements, UPI exports,<br>GPay, PhonePe, Paytm", "#7c3aed"),
        ("🧠", "Get Insights", "Spending patterns, behavioral<br>analysis, risk detection", "#6366f1"),
        ("💡", "Take Action", "Personalised recommendations<br>to improve your finances", "#8b5cf6"),
    ]
    for col, (icon, title, desc, color) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03);
                            border: 1px solid rgba(139,92,246,0.2);
                            border-radius: 18px; padding: 1.8rem 1.5rem;
                            text-align: center; backdrop-filter: blur(10px);
                            transition: all 0.3s;'>
                    <div style='font-size: 2.2rem;
                                filter: drop-shadow(0 0 8px {color}88);
                                margin-bottom: 0.8rem;'>{icon}</div>
                    <div style='font-weight: 700; color: #ffffff;
                                font-size: 1rem; margin-bottom: 0.5rem;'>{title}</div>
                    <div style='font-size: 0.78rem; color: #6d5fa6;
                                line-height: 1.5;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Upload a CSV file from the sidebar to get started.")
    st.stop()

# ── LOAD & CLEAN DATA ─────────────────────────────────
df = pd.read_csv(uploaded_file)
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

# Shared chart layout for dark galaxy theme
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(10,5,30,0.0)',
    plot_bgcolor='rgba(10,5,30,0.0)',
    font=dict(color='#a78bfa', family='Inter'),
    title_font=dict(color='#ffffff', size=16, family='Inter'),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a78bfa')),
    xaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)'),
    yaxis=dict(gridcolor='rgba(139,92,246,0.12)', color='#6d5fa6',
               linecolor='rgba(139,92,246,0.2)'),
)

GALAXY_COLORS = ['#7c3aed', '#6366f1', '#a78bfa', '#4f46e5',
                 '#8b5cf6', '#c4b5fd', '#312e81', '#5b21b6']

def chart_card(fig, col=None):
    fig.update_layout(**CHART_LAYOUT)
    if col:
        col.plotly_chart(fig, use_container_width=True)
    else:
        st.plotly_chart(fig, use_container_width=True)

# ── PAGE: OVERVIEW ────────────────────────────────────
if selected == "📊 Overview":
    st.markdown("""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;'>
            ✦ Financial Snapshot
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💸 Total Spending", f"₹{round(total_spending):,}")
    c2.metric("📈 Avg per Transaction", f"₹{round(avg_spending):,}")
    c3.metric("🔥 Highest Expense", f"₹{round(highest_expense):,}")
    c4.metric("🧾 Total Transactions", transaction_count)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;'>
            ✦ Transaction Log
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=350)

# ── PAGE: ANALYTICS ───────────────────────────────────
elif selected == "📈 Analytics":
    st.markdown("""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;'>
            ✦ Spending Analytics
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if 'category' in df.columns:
        category_data = df.groupby('category')['amount'].sum().reset_index()
        fig1 = px.bar(
            category_data, x='category', y='amount',
            title="Spending by Category",
            color='amount',
            color_continuous_scale=[[0, '#312e81'], [0.5, '#6366f1'], [1, '#a78bfa']],
        )
        fig1.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        fig1.update_layout(coloraxis_showscale=False)
        chart_card(fig1, col1)

    if 'merchant' in df.columns:
        merchant_data = (df.groupby('merchant')['amount'].sum()
                        .reset_index().sort_values('amount', ascending=True).tail(10))
        fig2 = px.bar(
            merchant_data, x='amount', y='merchant',
            orientation='h', title="Top Merchants",
            color='amount',
            color_continuous_scale=[[0, '#4f46e5'], [0.5, '#7c3aed'], [1, '#c4b5fd']],
        )
        fig2.update_traces(marker_line_color='rgba(139,92,246,0.3)', marker_line_width=1)
        fig2.update_layout(coloraxis_showscale=False)
        chart_card(fig2, col2)

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
            name='Daily Spend'
        ))
        fig3.update_layout(title="Daily Spending Trend", showlegend=False)
        chart_card(fig3)

    if 'category' in df.columns:
        fig4 = px.pie(
            df.groupby('category')['amount'].sum().reset_index(),
            values='amount', names='category',
            title="Category Breakdown",
            color_discrete_sequence=GALAXY_COLORS,
            hole=0.45
        )
        fig4.update_traces(
            textfont=dict(color='white'),
            marker=dict(line=dict(color='rgba(10,5,30,0.8)', width=2))
        )
        chart_card(fig4)

# ── PAGE: BEHAVIOR ────────────────────────────────────
elif selected == "🧠 Behavior":
    st.markdown("""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;'>
            ✦ Behavioral Analysis
        </div>
    """, unsafe_allow_html=True)

    if 'hour' in df.columns:
        df['impulsive'] = (df['hour'] >= 22) | (df['amount'] > 700)
        impulsive_count = int(df['impulsive'].sum())
        normal_count = transaction_count - impulsive_count

        col1, col2, col3 = st.columns(3)
        col1.metric("⚠️ Impulsive Purchases", impulsive_count)
        col2.metric("✅ Normal Purchases", normal_count)
        col3.metric("📊 Impulsive Rate",
                    f"{round(impulsive_count/transaction_count*100)}%")

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        fig4 = go.Figure(go.Pie(
            labels=['Impulsive', 'Normal'],
            values=[impulsive_count, normal_count],
            hole=0.5,
            marker=dict(
                colors=['#f87171', '#6366f1'],
                line=dict(color='rgba(10,5,30,0.8)', width=2)
            ),
            textfont=dict(color='white')
        ))
        fig4.update_layout(title="Spending Behaviour")
        chart_card(fig4, col1)

        if 'time_period' in df.columns:
            time_data = df.groupby('time_period')['amount'].sum().reset_index()
            fig5 = px.bar(
                time_data, x='time_period', y='amount',
                title="Spending by Time of Day",
                color='time_period',
                color_discrete_map={
                    'Morning': '#fbbf24',
                    'Afternoon': '#6366f1',
                    'Evening': '#34d399',
                    'Night': '#f87171'
                }
            )
            fig5.update_layout(showlegend=False)
            chart_card(fig5, col2)
    else:
        st.info("Add an 'hour' column (0–23) to your CSV to unlock behavioral insights.")

# ── PAGE: RECOMMENDATIONS ─────────────────────────────
elif selected == "💡 Recommendations":
    st.markdown("""
        <div style='font-size:0.72rem; color:#7c3aed; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;'>
            ✦ Smart Recommendations
        </div>
    """, unsafe_allow_html=True)

    recommendations = []

    if avg_spending > 700:
        recommendations.append(("💡", "High Average Spend",
            f"Your average transaction is ₹{round(avg_spending):,}. Consider a monthly spending cap.",
            "#7c3aed"))

    if 'merchant' in df.columns:
        top_merchant = df.groupby('merchant')['amount'].sum().idxmax()
        top_amount = df.groupby('merchant')['amount'].sum().max()
        recommendations.append(("🛍️", f"Top Merchant: {top_merchant}",
            f"You spent ₹{round(top_amount):,} here. Worth tracking closely.",
            "#6366f1"))

    if 'hour' in df.columns:
        night_spend = df[df['hour'] >= 22]['amount'].sum()
        if night_spend > 0:
            recommendations.append(("🌙", "Late Night Spending",
                f"₹{round(night_spend):,} spent after 10pm — often impulsive. Try a cut-off rule.",
                "#8b5cf6"))

    if transaction_count > 20:
        recommendations.append(("📊", "Transaction Volume",
            f"{transaction_count} transactions recorded. Weekly budget reviews can help catch patterns early.",
            "#4f46e5"))

    if not recommendations:
        st.success("🎉 Healthy spending pattern detected! Keep it up.")
    else:
        for icon, title, text, color in recommendations:
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03);
                            border: 1px solid rgba(139,92,246,0.25);
                            border-left: 4px solid {color};
                            border-radius: 14px; padding: 1.2rem 1.5rem;
                            margin-bottom: 1rem; backdrop-filter: blur(10px);'>
                    <div style='font-weight: 700; color: #ffffff;
                                margin-bottom: 0.4rem; font-size: 0.95rem;'>
                        {icon} {title}
                    </div>
                    <div style='color: #9ca3af; font-size: 0.87rem;
                                line-height: 1.6;'>{text}</div>
                </div>
            """, unsafe_allow_html=True)
