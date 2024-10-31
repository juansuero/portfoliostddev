import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Portfolio Standard Deviation and Diversification Checker")

# Step 1: User Inputs
st.header("Enter Your Portfolio Holdings")

# User inputs tickers and quantities
tickers = st.text_input("Enter Ticker Symbols (separated by commas)").split(',')
shares = st.text_input("Enter Shares Owned for Each Ticker (in same order, separated by commas)").split(',')

# Validate user inputs
try:
    shares = [float(s) for s in shares]
    tickers = [t.strip().upper() for t in tickers]
    if len(tickers) != len(shares):
        st.error("Please ensure each ticker has a corresponding share amount.")
    else:
        # Step 2: Data Retrieval
        st.subheader("Fetching Stock Data...")
        
        # Download data for tickers
        data = yf.download(tickers, period="1y")['Adj Close']
        
        # Calculate daily returns
        daily_returns = data.pct_change().dropna()
        
        # Step 3: Daily Standard Deviation and Correlation Matrix
        st.subheader("Daily Standard Deviation and Correlation Matrix")
        
        # Calculate daily standard deviation for each ticker
        daily_std = daily_returns.std()
        
        # Display individual daily standard deviations
        st.write("Daily Standard Deviation of Each Stock:")
        st.write(daily_std)
        
        # Correlation matrix for diversification insights
        corr_matrix = daily_returns.corr()
        st.write("Correlation Matrix:")
        st.write(corr_matrix)
        
        # Step 4: Portfolio Standard Deviation Calculation
        st.subheader("Portfolio Standard Deviation")
        
        # Calculate weights based on the number of shares and current prices
        total_value = sum(shares[i] * data[tickers[i]].iloc[-1] for i in range(len(tickers)))
        weights = [shares[i] * data[tickers[i]].iloc[-1] / total_value for i in range(len(tickers))]
        
        # Portfolio standard deviation
        port_variance = np.dot(weights, np.dot(daily_returns.cov(), weights))
        port_std = np.sqrt(port_variance)
        
        st.write(f"Portfolio Standard Deviation: {port_std:.4f}")
        
        # Step 5: Visualization of Correlation Matrix
        st.subheader("Correlation Matrix Heatmap")
        fig, ax = plt.subplots()
        cax = ax.matshow(corr_matrix, cmap="coolwarm")
        fig.colorbar(cax)
        plt.xticks(range(len(tickers)), tickers, rotation=90)
        plt.yticks(range(len(tickers)), tickers)
        st.pyplot(fig)
        
except Exception as e:
    st.error(f"Error: {e}")
