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
.stApp { background-color: #F6F8FC; }
.block-container { padding-top: 2rem; padding-left: 3rem; padding-right: 3rem; }
[data-testid="stSidebar"] { background: white; border-right: 1px solid #EAEAEA; }
.recommend-box {
    background: linear-gradient(135deg, #EEF4FF, #FFFFFF);
    padding: 18px; border-radius: 18px;
    margin-bottom: 12px; border-left: 5px solid #2563EB;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 💰 Riko — Personal Finance Intelligence")
st.markdown("AI-powered spending intelligence dashboard")

with st.sidebar:
    st.markdown("## Navigation")
    selected = st.radio(
        "Go to",
        ["Overview", "Analytics", "Behavior", "Recommendations"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a financial transaction CSV file to begin.")
    st.stop()

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

if selected == "Overview":
    st.subheader("Financial Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💸 Total Spending", f"₹{round(total_spending)}")
    c2.metric("📈 Avg Spend", f"₹{round(avg_spending)}")
    c3.metric("🔥 Highest Expense", f"₹{round(highest_expense)}")
    c4.metric("🧾 Transactions", transaction_count)
    st.markdown("### Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

elif selected == "Analytics":
    st.subheader("Spending Analytics")
    col1, col2 = st.columns(2)
    if 'category' in df.columns:
        category_data = df.groupby('category')['amount'].sum().reset_index()
        fig1 = px.bar(category_data, x='category', y='amount', title="Category Spending")
        col1.plotly_chart(fig1, use_container_width=True)
    if 'merchant' in df.columns:
        merchant_data = (df.groupby('merchant')['amount'].sum()
                        .reset_index().sort_values('amount', ascending=False).head(10))
        fig2 = px.bar(merchant_data, x='merchant', y='amount', title="Top Merchants")
        col2.plotly_chart(fig2, use_container_width=True)
    if 'date' in df.columns:
        daily = df.groupby('date')['amount'].sum().reset_index()
        fig3 = px.line(daily, x='date', y='amount', markers=True, title="Daily Spending Trend")
        st.plotly_chart(fig3, use_container_width=True)

elif selected == "Behavior":
    st.subheader("Behavioral Analytics")
    if 'hour' in df.columns:
        df['impulsive'] = (df['hour'] >= 22) | (df['amount'] > 700)
        impulsive_count = df['impulsive'].sum()
        st.metric("⚠️ Impulsive Purchases", impulsive_count)
        fig4 = px.pie(df, names='impulsive', title="Impulsive Spending")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Upload a dataset with an 'hour' column to see behavioral insights.")

elif selected == "Recommendations":
    st.subheader("Smart Recommendations")
    recommendations = []
    if avg_spending > 700:
        recommendations.append("💡 Your average spending is high. Consider setting a monthly cap.")
    if 'merchant' in df.columns:
        top_merchant = df.groupby('merchant')['amount'].sum().idxmax()
        recommendations.append(f"🛍️ Highest spending at {top_merchant}. Monitor expenses there.")
    if not recommendations:
        st.success("Healthy spending pattern detected! 🎉")
    else:
        for rec in recommendations:
            st.markdown(f"<div class='recommend-box'>{rec}</div>", unsafe_allow_html=True)
