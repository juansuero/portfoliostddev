import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re

def is_valid_isin(isin):
    """Validate ISIN format"""
    if not re.match(r'^[A-Z]{2}[A-Z0-9]{9}\d$', isin):
        return False
    return True

def calculate_portfolio_std(data, weights):
    """
    Calculate portfolio standard deviation and correlation matrix
    
    Parameters:
    data (pd.DataFrame): Historical price data
    weights (np.array): Portfolio weights
    
    Returns:
    float: Portfolio standard deviation (annualized, in percentage)
    pd.DataFrame: Correlation matrix
    """
    # Calculate daily returns
    returns = data.pct_change().dropna()
    
    # Calculate portfolio standard deviation (annualized)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    
    # Return standard deviation (as percentage) and correlation matrix
    return portfolio_std * 100, returns.corr()

def get_symbol(input_str):
    """Convert input to valid yfinance symbol"""
    input_str = input_str.strip().upper()
    if is_valid_isin(input_str):
        # For demonstration, you might want to use a proper ISIN lookup service
        try:
            # Some funds might need .DE, .L etc. suffix based on exchange
            ticker = yf.Ticker(input_str)
            if hasattr(ticker, 'info'):
                return input_str
        except:
            st.error(f"Could not find ticker for ISIN: {input_str}")
            return None
    return input_str

st.title('Portfolio Standard Deviation Calculator')

# Input format selection
input_format = st.radio(
    "Select input format",
    ["Ticker Symbol", "ISIN"],
    help="Choose whether to input ticker symbols (e.g., AAPL) or ISIN numbers (e.g., US0378331005)"
)

# Example placeholder based on selection
placeholder = "AAPL, MSFT, GOOGL" if input_format == "Ticker Symbol" else "US0378331005, US5949181045, US02079K3059"
symbols = st.text_input(
    f'Enter {"ticker symbols" if input_format == "Ticker Symbol" else "ISIN numbers"} (comma separated)', 
    placeholder
)

input_method = st.radio('Select input method', ('Number of shares', 'Weight in percentages'))
period = st.selectbox('Select the period for historical data', ['1y', '2y', '5y', '10y', 'ytd', 'max'])

if input_method == 'Number of shares':
    shares = st.text_input('Enter the number of shares for each holding (comma separated)', '10.13, 15.5, 20.75')
else:
    weights = st.text_input('Enter the weight in percentages for each holding (comma separated)', '30, 40, 30')

if st.button('Calculate'):
    # Process inputs
    inputs = [s.strip() for s in symbols.split(',')]
    tickers = []
    
    # Convert inputs to valid symbols
    for input_str in inputs:
        symbol = get_symbol(input_str)
        if symbol:
            tickers.append(symbol)
        else:
            st.stop()
    
    # Process weights/shares
    if input_method == 'Number of shares':
        shares = [float(share.strip()) for share in shares.split(',')]
        total_shares = np.sum(shares)
        weights = np.array(shares) / total_shares
    else:
        weights = [float(weight.strip()) for weight in weights.split(',')]
        if np.sum(weights) != 100:
            st.error('The weights must add up to 100%.')
            st.stop()
        weights = np.array(weights) / 100

    # Fetch data and calculate
    try:
        data = yf.download(tickers, period=period)['Adj Close']
        portfolio_std, corr_matrix = calculate_portfolio_std(data, weights)
        
        st.write(f'Standard Deviation of Portfolio: {portfolio_std:.2f}%')
        
        st.write('Correlation Matrix:')
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error calculating portfolio metrics: {str(e)}")