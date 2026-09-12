from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if not api_key:
    api_key = st.secrets["ALPHA_VANTAGE_API_KEY"]

st.title("📊 Real-Time Stock Market Dashboard")

st.write("Welcome to my Stock Market Dashboard!")

if api_key:
    st.success("API key loaded successfully!")
else:
    st.error("API key not found!")    

import requests
import pandas as pd

st.subheader("Select a Stock")

symbol = st.selectbox("choose a stock:",["IBM","AAPL","MSFT","GOOGL","AMZN"])

url = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": api_key
}

response = requests.get(url, params=params)
data = response.json()

if "Time Series (Daily)" in data:
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
else:
    st.error("Stock data is currently unavailable. Please try again later.")
    st.stop()
df=df.astype(float)
df.index = pd.to_datetime(df.index)
df=df.sort_index()
df.columns = ["Open","High","Low","Close","Volume"]

latest_close = df["Close"].iloc[-1]

latest_date = df.index[-1]
st.subheader("Market Summary")

st.metric("latest closing price",f"${latest_close:.2f}")

st.write("latest Trading Date:",latest_date)

latest_open = df["Open"].iloc[-1]
latest_high = df["High"].iloc[-1]
latest_low= df["Low"].iloc[-1]
latest_volume= df["Volume"].iloc[-1]
previous_close = df["Close"].iloc[-2]
price_change = latest_close - previous_close
price_change_percent = (price_change / previous_close)*100

col1, col2 = st.columns(2)
col1.metric("Price Change", f"${price_change:.2f}")
col2.metric("Percentage Change", f"{price_change_percent:.2f}%")

col3, col4 = st.columns(2)
col3.metric("Latest High Price", f"${latest_high:.2f}")
col4.metric("Latest Low Price", f"${latest_low:.2f}")

st.subheader("Historical Stock Date")
st.dataframe(df,use_container_width=True)

col5, col6 = st.columns(2)
col5.metric("Opening Price", f"${latest_open:.2f}")
col6.metric("Latest Trading Volume", f"{latest_volume:,.0f}")

import plotly.express as px
st.subheader("Closing Price Trend")

fig = px.line(df, x=df.index, y="Close", title=f"{symbol} Closing Price")
st.subheader("Trading Volume Trend")

st.plotly_chart(fig)
volume_fig = px.bar(
    df,
    x=df.index,
    y="Volume",
    title=f"{symbol} Trading Volume"
)

st.plotly_chart(volume_fig)


