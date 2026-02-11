import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Stock Dashboard")

st.title('Stock Dashboard')

ticker_input = st.text_input('Enter Ticker of Company of Choice (e.g., APPL, AMZN, HMC)')
st.caption("Don't know the ticker? Search '[Company Name] stock ticker' on Google")
st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>OR</p>", unsafe_allow_html=True)
ticker_dropdown = st.selectbox('Select Popular Companies From the Dropdown List', [
    'None',
    'AAPL - Apple Inc.',
    'AMZN - Amazon.com Inc.',
    'BAJFINANCE.NS - Bajaj Finance',
    'BHARTIARTL.NS - Bharti Airtel',
    'DIS - Walt Disney Company',
    'GOOGL - Alphabet Inc.',
    'HD - Home Depot',
    'HDFCBANK.NS - HDFC Bank',
    'HINDUNILVR.NS - Hindustan Unilever',
    'ICICIBANK.NS - ICICI Bank',
    'INFY.NS - Infosys',
    'ITC.NS - ITC Limited',
    'JNJ - Johnson & Johnson',
    'JPM - JPMorgan Chase & Co.',
    'META - Meta Platforms Inc.',
    'MSFT - Microsoft Corporation',
    'NVDA - NVIDIA Corporation',
    'PG - Procter & Gamble',
    'RELIANCE.NS - Reliance Industries',
    'SBIN.NS - State Bank of India',
    'TCS.NS - Tata Consultancy Services',
    'TSLA - Tesla Inc.',
    'UNH - UnitedHealth Group',
    'V - Visa Inc.',
    'WMT - Walmart Inc.',
], index=None, placeholder="Choose a company...")

# Determine which ticker to use
if ticker_input and ticker_dropdown:
    st.error('Please use either the text input OR dropdown, not both')
    st.stop()
elif ticker_input:
    ticker = ticker_input.upper()
elif ticker_dropdown:
    ticker = ticker_dropdown.split(' - ')[0]
else:
    st.info('Enter a stock ticker or select from dropdown to get started')
    st.stop()

if not ticker:
    st.info('Enter a stock ticker to get started')
    st.stop()

start_date = st.date_input(
    "Select Start Date",
    value=pd.to_datetime("2016-01-01"),
    max_value=pd.Timestamp.today()
)

end_date = st.date_input(
    "Select End Date",
    value=pd.Timestamp.today(),
    min_value=start_date,        # Cannot be before start date
    max_value=pd.Timestamp.today()  # Cannot exceed today
)

if start_date >= end_date:
    st.warning('Please select an end date that is after the start date')
    st.stop()

if not ticker:
    st.info('Enter a stock ticker and select date range to view data')
    st.stop()


data = yf.download(ticker, start=start_date, end=end_date)
data.columns = data.columns.get_level_values(0)  # YFinance gives 2-D data. Flatten columns to 1-D for Plotly
fig = px.line(data, x=data.index, y='Close', title=ticker, color_discrete_sequence=px.colors.diverging.RdYlGn)
st.plotly_chart(fig)

pricing_data, fundamental_data, news, openai1=st.tabs(["Pricing Data","Fundamental Data", "Top 10 News", "Groq"])

with pricing_data:
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Close']/data['Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*261*100
    st.write('Return in the selected period is', annual_return, '%')
    stdev = np.std(data2['% Change'])*np.sqrt(261)
    st.write('Standard Deviation is', stdev*100, '%')
    st.write('Risk Adj. Return is', annual_return/(stdev*100))

with fundamental_data:
    st.header('Fundamental Analysis')
    stock = yf.Ticker(ticker)
    
    st.subheader('Balance Sheet')
    st.write(stock.balance_sheet.T)
    
    st.subheader('Income Statement')
    st.write(stock.financials.T)
    
    st.subheader('Cash Flow Statement')
    st.write(stock.cashflow.T)


from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(f"**{df_news['title'][i]}**")
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

from groq import Groq
import os

# Use environment variable or Streamlit secrets
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))

with openai1:
    if not st.secrets.get("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not configured in secrets")
        st.stop()
    
    buy_reason, sell_reason, swot_analysis = st.tabs(["3 Reasons to Buy", "3 Reasons to Sell", "SWOT Analysis"])
    
    with buy_reason:
        st.subheader(f'3 reasons to BUY {ticker} stock')
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Give 3 reasons to buy {ticker} stock"}]
        )
        st.write(response.choices[0].message.content)
    
    with sell_reason:
        st.subheader(f'3 reasons to SELL {ticker} stock')
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Give 3 reasons to sell {ticker} stock"}]
        )
        st.write(response.choices[0].message.content)
    
    with swot_analysis:
        st.subheader(f'SWOT Analysis of {ticker} stock')
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Provide a SWOT analysis of {ticker} stock"}]
        )
        st.write(response.choices[0].message.content)