# Stock Dashboard

*"In God we trust. All others must bring data." — W. Edwards Deming*

</div>

---

## Objective

The goal of this project was to build an **interactive stock analysis dashboard** that provides:
- Real-time stock price visualization
- Financial metrics and risk analysis
- Fundamental data analysis
- Latest news with sentiment analysis

All in one place, accessible through a clean web interface.

---

## Features

### Price Movements & Analytics
- **Interactive Price Chart**: Visualize historical stock prices with Plotly
- **Performance Metrics**: 
  - Annual Return Calculation
  - Standard Deviation (Volatility)
  - Risk-Adjusted Return (Sharpe-like ratio)

### Fundamental Analysis
- **Balance Sheet**: Annual financial position
- **Income Statement**: Revenue and profitability metrics
- **Cash Flow Statement**: Operating, investing, and financing activities

### News & Sentiment
- Top 10 latest news articles
- **Sentiment Analysis** on titles and summaries
- Publication dates and article summaries

---

## Financial Calculations

### Annual Return
```python
annual_return = daily_percentage_change.mean() * 261 * 100
```
- Calculates average daily return
- Multiplies by 261 (average trading days per year)
- Converts to percentage

### Standard Deviation (Volatility)
```python
stdev = np.std(daily_percentage_change) * np.sqrt(261)
```
- Measures daily price fluctuation
- Annualized using square root of time rule
- Higher value = higher risk

### Risk-Adjusted Return
```python
risk_adj_return = annual_return / (stdev * 100)
```
- Similar to Sharpe Ratio (without risk-free rate)
- Measures return per unit of risk
- Higher value = better risk-adjusted performance

---

## Getting Started

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/its-srishti/Stock-Dashboard.git
cd stock-dashboard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run Stock_Dashboard.py
```


---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web application framework |
| **yfinance** | Stock data retrieval |
| **Plotly** | Interactive charts |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical computations |
| **StockNews** | News & sentiment analysis |

---

## Known Issues & Solutions

### Alpha Vantage API Limitations

**Problem**: Free Alpha Vantage API has a 25 requests/day limit, which is insufficient for regular use.

**Solution**: This project uses **yfinance** instead, which provides:
- ✅ Unlimited free requests
- ✅ No API key required
- ✅ Real-time data
- ✅ Comprehensive fundamental data

### Premium Alpha Vantage Users

If you have **Premium Alpha Vantage access**, you can use this alternative code for fundamental data:

<details>
<summary><b>Click to expand Alpha Vantage code</b></summary>

```python
from alpha_vantage.fundamentaldata import FundamentalData

with fundamental_data:
    st.header('Fundamental Analysis')
    key = 'YOUR_PREMIUM_API_KEY'  # Replace with your key
    fd = FundamentalData(key, output_format='pandas')
    
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
```

**Additional requirement**: Add to `requirements.txt`
```
alpha-vantage
```

</details>

---

## Usage

1. **Enter Stock Ticker** (e.g., AAPL, GOOGL, TSLA)
2. **Select Date Range** using the sidebar
3. **Explore Three Tabs**:
   - Pricing Data: View returns and risk metrics
   - Fundamental Data: Analyze financial statements
   - Top 10 News: Read latest news with sentiment

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [yfinance](https://github.com/ranaroussi/yfinance) for financial data
- [Plotly](https://plotly.com/) for interactive visualizations

