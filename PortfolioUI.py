import streamlit as st
import pandas as pd

from Repository import PortfolioRepository

portfolio = PortfolioRepository.get_portfolio('largeCap')
df = pd.DataFrame()

for element in portfolio.get_portfolio_elements():
    row = pd.DataFrame([{
        'Symbol': element.asset.symbol,
        'Numeraire': portfolio.numeraire,
        'Purchase_period': portfolio.purchase_period,
        'Volume': element.volume,
        'Period_start': element.period_start,
        'Period_end': element.period_end}])

    df = pd.concat([df, row], ignore_index=True)

# Streamlit commands to display the web app
st.title(portfolio.name)
st.write("This is a simple data table:")

# Display the DataFrame as a table in Streamlit
st.table(df)
