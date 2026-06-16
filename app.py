import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Riko — Finance Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #fafafa 100%);
}

/* Remove top padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e8ecf0 !important;
}

[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.3rem;
}

[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    cursor: pointer;
    font-size: 0.9rem;
    color: #374151;
    transition: all 0.2s;
    border: none;
    width: 100%;
    display: block;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #f3f4f6;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.5rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #f1f3f5;
}

[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #111827 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e8ecf0;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 14px;
    border: 2px dashed #c7d2fe;
    padding: 1rem;
}

/* Plotly charts */
.js-plotly-plot {
    border-radius: 16px;
    overflow: hidden;
}

/* Info/success boxes */
.stAlert {
    border-radius: 12px !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding-bottom: 1.5rem;'>
            <div style='font-size: 2.5rem;'>💰</div>
            <div style='font-size: 1.3rem; font-weight: 700; color: #111827;'>Riko</div>
            <div style='font-size: 0.75rem; color: #9ca3af; margin-top: 2px;'>Finance Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    selected = st.radio(
        "Navigation",
        ["📊 Overview", "📈 Analytics", "🧠 Behavior", "💡 Recommendations"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border:none; border-top:1px solid #f1f3f5; margin: 1rem 0;'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your CSV",
        type=["csv"],
        help="Upload a transaction CSV file (date, amount, category, merchant)"
    )

    st.markdown("""
        <div style='margin-top: 1rem; padding: 0.8rem; background: #f8faff;
                    border-radius: 10px; border: 1px solid #e0e7ff;'>
            <div style='font-size: 0.75rem; color: #6366f1; font-weight: 600;'>
                💡 Sample columns
            </div>
            <div style='font-size: 0.7rem; color: #9ca3af; margin-top: 4px;'>
                date, amount, category,<br>merchant, hour
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────
st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 2rem; font-weight: 700; color: #111827; margin: 0;'>
            Personal Finance Intelligence
        </h1>
        <p style='color: #6b7280; margin: 0.3rem 0 0 0; font-size: 0.95rem;'>
            Upload your transaction data and get AI-powered spending insights
        </p>
    </div>
""", unsafe_allow_html=True)

# ── NO FILE STATE ─────────────────────────────────────
if uploaded_file is None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style='background:white; border-radius:16px; padding:1.5rem;
                        box-shadow:0 2px 12px rgba(0,0,0,0.06); text-align:center;'>
                <div style='font-size:2rem'>📂</div>
                <div style='font-weight:600; color:#111827; margin-top:0.5rem;'>Upload CSV</div>
                <div style='font-size:0.8rem; color:#9ca3af; margin-top:0.3rem;'>
                    Bank statements, UPI exports, GPay, PhonePe
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='background:white; border-radius:16px; padding:1.5rem;
                        box-shadow:0 2px 12px rgba(0,0,0,0.06); text-align:center;'>
                <div style='font-size:2rem'>🧠</div>
                <div style='font-weight:600; color:#111827; margin-top:0.5rem;'>Get Insights</div>
                <div style='font-size:0.8rem; color:#9ca3af; margin-top:0.3rem;'>
                    Spending patterns, behavioral analysis, risk detection
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style='background:white; border-radius:16px; padding:1.5rem;
                        box-shadow:0 2px 12px rgba(0,0,0,0.06); text-align:center;'>
                <div style='font-size:2rem'>💡</div>
                <div style='font-weight:600; color:#111827; margin-top:0.5rem;'>Take Action</div>
                <div style='font-size:0.8rem; color:#9ca3af; margin-top:0.3rem;'>
                    Personalised recommendations to improve finances
                </div>
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

# ── PAGE: OVERVIEW ────────────────────────────────────
if selected == "📊 Overview":
    st.markdown("### Financial Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💸 Total Spending", f"₹{round(total_spending):,}")
    c2.metric("📈 Avg per Transaction", f"₹{round(avg_spending):,}")
    c3.metric("🔥 Highest Expense", f"₹{round(highest_expense):,}")
    c4.metric("🧾 Total Transactions", transaction_count)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Transaction Data")
    st.dataframe(df, use_container_width=True, height=350)

# ── PAGE: ANALYTICS ───────────────────────────────────
elif selected == "📈 Analytics":
    st.markdown("### Spending Analytics")

    col1, col2 = st.columns(2)

    if 'category' in df.columns:
        category_data = df.groupby('category')['amount'].sum().reset_index()
        fig1 = px.bar(
            category_data, x='category', y='amount',
            title="Spending by Category",
            color='amount',
            color_continuous_scale='Blues',
            template='plotly_white'
        )
        fig1.update_layout(showlegend=False, coloraxis_showscale=False,
                           plot_bgcolor='white', paper_bgcolor='white')
        col1.plotly_chart(fig1, use_container_width=True)

    if 'merchant' in df.columns:
        merchant_data = (df.groupby('merchant')['amount'].sum()
                        .reset_index().sort_values('amount', ascending=False).head(10))
        fig2 = px.bar(
            merchant_data, x='amount', y='merchant',
            orientation='h', title="Top 10 Merchants",
            color='amount', color_continuous_scale='Purples',
            template='plotly_white'
        )
        fig2.update_layout(showlegend=False, coloraxis_showscale=False,
                           plot_bgcolor='white', paper_bgcolor='white')
        col2.plotly_chart(fig2, use_container_width=True)

    if 'date' in df.columns:
        daily = df.groupby('date')['amount'].sum().reset_index()
        fig3 = px.line(
            daily, x='date', y='amount',
            markers=True, title="Daily Spending Trend",
            template='plotly_white',
            color_discrete_sequence=['#6366f1']
        )
        fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        fig3.update_traces(line_width=2.5)
        st.plotly_chart(fig3, use_container_width=True)

# ── PAGE: BEHAVIOR ────────────────────────────────────
elif selected == "🧠 Behavior":
    st.markdown("### Behavioral Analytics")

    if 'hour' in df.columns:
        df['impulsive'] = (df['hour'] >= 22) | (df['amount'] > 700)
        impulsive_count = int(df['impulsive'].sum())
        normal_count = transaction_count - impulsive_count

        col1, col2 = st.columns(2)
        col1.metric("⚠️ Impulsive Purchases", impulsive_count)
        col2.metric("✅ Normal Purchases", normal_count)

        fig4 = px.pie(
            values=[impulsive_count, normal_count],
            names=['Impulsive', 'Normal'],
            title="Spending Behaviour Breakdown",
            color_discrete_sequence=['#f87171', '#6366f1'],
            template='plotly_white',
            hole=0.4
        )
        fig4.update_layout(paper_bgcolor='white')
        st.plotly_chart(fig4, use_container_width=True)

        if 'time_period' in df.columns:
            time_data = df.groupby('time_period')['amount'].sum().reset_index()
            fig5 = px.bar(
                time_data, x='time_period', y='amount',
                title="Spending by Time of Day",
                color='time_period',
                color_discrete_sequence=['#fbbf24','#6366f1','#34d399','#f87171'],
                template='plotly_white'
            )
            fig5.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Add an 'hour' column (0–23) to your CSV to see behavioral insights.")

# ── PAGE: RECOMMENDATIONS ─────────────────────────────
elif selected == "💡 Recommendations":
    st.markdown("### Smart Recommendations")

    recommendations = []

    if avg_spending > 700:
        recommendations.append(("💡", "High Average Spend",
            "Your average transaction is above ₹700. Consider setting a monthly spending cap."))

    if 'merchant' in df.columns:
        top_merchant = df.groupby('merchant')['amount'].sum().idxmax()
        top_amount = df.groupby('merchant')['amount'].sum().max()
        recommendations.append(("🛍️", f"Top Merchant: {top_merchant}",
            f"You spent ₹{round(top_amount):,} at {top_merchant}. Monitor expenses here."))

    if 'hour' in df.columns:
        night_spend = df[df['hour'] >= 22]['amount'].sum()
        if night_spend > 0:
            recommendations.append(("🌙", "Late Night Spending",
                f"₹{round(night_spend):,} spent after 10pm. These are often impulsive purchases."))

    if transaction_count > 50:
        recommendations.append(("📊", "High Transaction Volume",
            f"{transaction_count} transactions recorded. Consider weekly budget reviews."))

    if not recommendations:
        st.success("🎉 Great job! Your spending looks healthy.")
    else:
        for icon, title, text in recommendations:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #eef2ff, #ffffff);
                            padding: 1.2rem 1.5rem; border-radius: 14px;
                            margin-bottom: 1rem; border-left: 4px solid #6366f1;'>
                    <div style='font-weight: 600; color: #111827; margin-bottom: 0.3rem;'>
                        {icon} {title}
                    </div>
                    <div style='color: #6b7280; font-size: 0.9rem;'>{text}</div>
                </div>
            """, unsafe_allow_html=True)
