import pandas as pd


def clean_data(df):

    # lowercase columns
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    # remove duplicates
    df.drop_duplicates(
        inplace=True
    )

    # clean dates
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(
            df['date'],
            errors='coerce'
        )

    return df
