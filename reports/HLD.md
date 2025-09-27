# High-Level Design: Crypto Liquidity Prediction System

## System Overview
A machine learning system that predicts cryptocurrency liquidity levels to identify potential market instability risks.

## Architecture
Data Sources → Data Processing → ML Model → Prediction API → User Interface
↓ ↓ ↓ ↓ ↓
CSV Files Cleaning & Random Streamlit Web Dashboard
Feature Eng. Forest FastAPI


## Components
1. **Data Layer**: Historical crypto price/volume data
2. **Processing Layer**: Pandas for data cleaning and feature engineering
3. **ML Layer**: Scikit-learn models for liquidity prediction
4. **API Layer**: Streamlit for web interface
5. **Presentation Layer**: Web dashboard with risk indicators

## Data Flow
1. User inputs crypto metrics → 2. System processes features → 
3. Model predicts liquidity ratio → 4. System assesses risk level → 
5. Results displayed to user