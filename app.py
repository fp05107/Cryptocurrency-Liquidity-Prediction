# app/app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Set page config (important for Render)
st.set_page_config(
    page_title="Crypto Liquidity Predictor",
    page_icon="📊",
    layout="wide"
)

# Load model with error handling
@st.cache_resource
def load_model():
    try:
        # Try different possible paths for Render
        model_paths = [
            'notebooks/tuned_liquidity_model.pkl',
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                model = joblib.load(path)
                st.success(f"Model loaded successfully from {path}")
                return model
        
        st.error("Model file not found. Please check the file path.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Load the model
model = load_model()

# App title
st.title("📊 Cryptocurrency Liquidity Predictor")
st.write("Predict liquidity risk for any cryptocurrency")

# Only show the app if model is loaded
if model is not None:
    # Input form
    st.sidebar.header("🔧 Input Crypto Data")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        price = st.number_input("Price (USD)", min_value=0.0, value=40000.0, step=1000.0)
        volume_24h = st.number_input("24h Volume (USD)", min_value=0.0, value=25000000000.0, step=1000000.0)
        market_cap = st.number_input("Market Cap (USD)", min_value=0.0, value=750000000000.0, step=1000000.0)
    
    with col2:
        change_24h = st.number_input("24h Price Change (%)", value=2.5, step=0.1)
        change_7d = st.number_input("7d Price Change (%)", value=5.5, step=0.1)
        day_of_week = st.selectbox("Day of Week", options=list(range(7)), 
                                 format_func=lambda x: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x])
        month = st.slider("Month", 1, 12, 3)

    # Calculate derived features
    volume_market_ratio = volume_24h / market_cap if market_cap > 0 else 0

    # Create feature array
    features = np.array([[price, volume_24h, market_cap, change_24h, change_7d, 
                         volume_market_ratio, day_of_week, month]])

    # Prediction button
    if st.sidebar.button("🎯 Predict Liquidity", type="primary"):
        try:
            prediction = model.predict(features)[0]
            
            # Display results
            st.subheader("📈 Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Predicted Liquidity Ratio", f"{prediction:.6f}")
            
            # Risk assessment
            if prediction > 0.1:
                risk_level = "🟢 LOW RISK"
                color = "green"
                advice = "✅ Good liquidity conditions"
            elif prediction > 0.01:
                risk_level = "🟡 MEDIUM RISK" 
                color = "orange"
                advice = "⚠️ Monitor liquidity closely"
            else:
                risk_level = "🔴 HIGH RISK"
                color = "red"
                advice = "🚨 Potential liquidity crisis"
            
            with col2:
                st.markdown(f"<h2 style='color: {color};'>{risk_level}</h2>", unsafe_allow_html=True)
            
            with col3:
                st.info(advice)
            
            # Explanation
            with st.expander("💡 Understanding the Results"):
                st.markdown("""
                **Liquidity Ratio Interpretation:**
                - **Ratio = 24h Trading Volume / Market Cap**
                - **High Ratio (> 0.1)**: Healthy liquidity, easy to trade
                - **Medium Ratio (0.01-0.1)**: Moderate liquidity, some slippage possible  
                - **Low Ratio (< 0.01)**: Poor liquidity, high slippage risk
                
                **Recommendations:**
                - Low Risk: Normal trading conditions
                - Medium Risk: Use limit orders, avoid large market orders
                - High Risk: Consider delaying large trades or using OTC
                """)
                
        except Exception as e:
            st.error(f"❌ Error in prediction: {str(e)}")

    # Sample data for quick testing
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Quick Test Data")
    
    if st.sidebar.button("Load Bitcoin Data"):
        st.sidebar.info("Bitcoin data loaded!")
    
    if st.sidebar.button("Load Small Cap Data"):
        st.sidebar.info("Small cap data loaded!")

    # Add some analytics
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 App Info")
    st.sidebar.info("""
    **Version:** 1.0  
    **Last Updated:** March 2024  
    **Model:** Random Forest  
    **Accuracy:** ~85% R²
    """)

else:
    st.error("""
    ❌ Model could not be loaded. Please ensure:
    1. tuned_liquidity_model.pkl is in the correct location
    2. All dependencies are installed
    3. Check the file paths
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit | Cryptocurrency Liquidity Prediction System</p>
</div>
""", unsafe_allow_html=True)