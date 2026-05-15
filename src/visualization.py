%%writefile personal-finance-intelligence-system/src/visualization.py

import plotly.express as px


def category_chart(df):

    category_data = (
        df.groupby('category')
        ['amount']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_data,
        x='category',
        y='amount',
        title='Category Spending'
    )

    return fig
