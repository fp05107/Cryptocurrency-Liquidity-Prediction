# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Load the trained model
model = joblib.load('notebooks/tuned_liquidity_model.pkl')

# App title
st.title("Cryptocurrency Liquidity Predictor")
st.write("Predict liquidity risk for any cryptocurrency")

# Input form
st.sidebar.header("Input Crypto Data")

price = st.sidebar.number_input("Price (USD)", min_value=0.0, value=1000.0)
volume_24h = st.sidebar.number_input("24h Volume (USD)", min_value=0.0, value=50000000.0)
market_cap = st.sidebar.number_input("Market Cap (USD)", min_value=0.0, value=1000000000.0)
change_24h = st.sidebar.number_input("24h Price Change (%)", value=0.0)
change_7d = st.sidebar.number_input("7d Price Change (%)", value=0.0)
day_of_week = st.sidebar.selectbox("Day of Week", options=list(range(7)), format_func=lambda x: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][x])
month = st.sidebar.slider("Month", 1, 12, 1)

# Calculate derived features
volume_market_ratio = volume_24h / market_cap if market_cap > 0 else 0

# Create feature array
features = np.array([[price, volume_24h, market_cap, change_24h, change_7d, 
                     volume_market_ratio, day_of_week, month]])

# Prediction
if st.sidebar.button("Predict Liquidity"):
    try:
        prediction = model.predict(features)[0]
        
        # Display results
        st.subheader("Prediction Results")
        st.metric("Predicted Liquidity Ratio", f"{prediction:.6f}")
        
        # Risk assessment
        if prediction > 0.1:
            risk_level = "LOW RISK"
            color = "green"
        elif prediction > 0.01:
            risk_level = "MEDIUM RISK"
            color = "orange"
        else:
            risk_level = "HIGH RISK"
            color = "red"
            
        st.markdown(f"<h3 style='color: {color};'>Liquidity Risk: {risk_level}</h3>", 
                   unsafe_allow_html=True)
        
        # Interpretation
        st.info("""
        **Interpretation:**
        - Liquidity Ratio = 24h Volume / Market Cap
        - Higher ratio = Better liquidity = Lower risk
        - Lower ratio = Poor liquidity = Higher risk
        """)
        
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")

# Add some information
st.sidebar.markdown("---")
st.sidebar.info("""
**How to use:**
1. Enter cryptocurrency data
2. Click 'Predict Liquidity'
3. View risk assessment
""")

# Sample data for testing
st.subheader("Sample Data for Testing")
sample_data = {
    'Bitcoin (High Liquidity)': [40000, 25000000000, 750000000000, 2.5, 5.5, 0],
    'Small Cap Coin (Risk)': [0.50, 50000, 1000000, -5.0, -15.0, 0]
}

for coin, values in sample_data.items():
    if st.button(f"Load {coin} Data"):
        st.sidebar.number_input("Price (USD)", value=values[0])
        st.sidebar.number_input("24h Volume (USD)", value=values[1])
        st.sidebar.number_input("Market Cap (USD)", value=values[2])
        st.sidebar.number_input("24h Price Change (%)", value=values[3])
        st.sidebar.number_input("7d Price Change (%)", value=values[4])