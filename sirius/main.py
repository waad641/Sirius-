import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
# Define the list of coins
coins = ['BTC-USD', 'ETH-USD']
# Define the date range 
start_date = '2022-01-01'
end_date = '2022-01-31'
# Get the close prices for each coin
close_prices = {}
for coin in coins:
    data = yf.download(coin, start=start_date, end=end_date, group_by='ticker')
    close_prices[coin] = data['Close']
# Combine the close prices into a single DataFrame
df = pd.concat(close_prices, axis=1)
df.columns = coins
# Display the DataFrame
st.write(df)
# Create a chart with two lines
chart = alt.Chart(df.reset_index()).transform_fold(
    coins,
    as_=['coin', 'price']
).mark_line().encode(
    x='Date:T',
    y='price:Q',
    color='coin:N'
).properties(
    width=800,
    height=400
)
st.altair_chart(chart)