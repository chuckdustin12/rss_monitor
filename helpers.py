
def get_cik_by_ticker(df, ticker):

    row = df[df['ticker'] == ticker]
    if not row.empty:
        return row.iloc[0]['cik']
    else:
        return None
