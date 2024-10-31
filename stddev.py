# Install necessary libraries
# !pip install streamlit yfinance pandas numpy seaborn matplotlib

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to fetch historical data
def fetch_data(tickers):
    data = yf.download(tickers, period='5y')['Adj Close']
    return data

# Function to calculate portfolio standard deviation
def calculate_portfolio_std(data, shares):
    returns = data.pct_change().dropna()
    weights = np.array(shares) / np.sum(shares)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_std * 100, returns.corr()  # Convert to percentage

# Streamlit app
st.title('Portfolio Standard Deviation Calculator')

# User input for tickers and shares
tickers = st.text_input('Enter your holding tickers (comma separated)', 'AAPL, MSFT, GOOGL')
shares = st.text_input('Enter the number of shares for each ticker (comma separated)', '10.13, 15.5, 20.75')

if st.button('Calculate'):
    tickers = [ticker.strip() for ticker in tickers.split(',')]
    shares = [float(share.strip()) for share in shares.split(',')]
    
    data = fetch_data(tickers)
    portfolio_std, corr_matrix = calculate_portfolio_std(data, shares)
    
    st.write(f'Daily Standard Deviation of Portfolio: {portfolio_std:.2f}%')
    
    st.write('Correlation Matrix:')
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)