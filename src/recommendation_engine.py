%%writefile personal-finance-intelligence-system/src/recommendation_engine.py

def generate_recommendations(df):

    recommendations = []

    avg_spending = (
        df['amount']
        .mean()
    )

    if avg_spending > 700:

        recommendations.append(
            "Your spending is relatively high. Consider setting a monthly budget."
        )

    if 'merchant' in df.columns:

        top_merchant = (
            df.groupby('merchant')
            ['amount']
            .sum()
            .idxmax()
        )

        recommendations.append(
            f"Highest spending occurs at {top_merchant}. Consider tracking expenses there."
        )

    return recommendations
