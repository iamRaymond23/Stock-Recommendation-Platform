#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# List of Indian stocks
stock_list = [
    'COFFEEDAY', 'PKTEA', 'USHAMART', 'IOC', 'SATIA',
    'BHARTIARTL', 'TVSSRICHAK', 'AMRUTANJAN', 'DGCONTENT',
    'INDLMETER', 'M&M', 'TIRUMALCHM', 'BALLARPUR', 'HATHWAY', 'ITC'
]

# Function to categorize investors based on their risk profile
def categorize_investor(income, investment_amount, expected_return):
    score = 0
    # Income Level Scoring
    if income > 1000000:
        score += 1
    elif income < 500000:
        score += 2
    # Investment Amount Scoring
    if investment_amount > 200000:
        score += 2
    elif investment_amount < 50000:
        score += 1
    # Expected Rate of Return
    if expected_return == '>10%':
        score += 2
    elif expected_return == '5-10%':
        score += 1
    # Categorize investors based on their risk profile
    if score >= 6:
        return 'Aggressive'
    elif score >= 3:
        return 'Moderate'
    else:
        return 'Conservative'

# Function to fetch stock data
def fetch_stock_data(stock):
    try:
        # Set up End and Start times for data grab
        end = pd.Timestamp.today()
        start = end - pd.DateOffset(years=1)
        # Fetch data for the stock
        company = yf.download(f"{stock}.NS", start, end)
        return company
    except Exception as e:
        st.error(f"Error fetching stock data: {str(e)}")

# Page title
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #FFFF00;
            text-align: center;
            margin-bottom: 30px;
        }
        .tagline {
            font-size: 24px;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 50px;
        }
        .sidebar .sidebar-content {
            background-color: #000000;
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🚀 StockInvestor 📈</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Investing Made Exciting!</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Menu")
selected_page = st.sidebar.radio("Navigation", ["Home", "Login", "Signup", "Questionnaire", "Stock Recommendation"])

# Placeholder for user data storage (Replace with your preferred method)
user_data = {}

# Placeholder for selected stock
selected_stock = None

# Home page
if selected_page == "Home":
    st.write("Welcome to StockInvestor!")
    st.write("StockInvestor, your go-to destination for stock market insights. Explore the markets effortlessly with our user-friendly platform and expert guidance. Whether you're a beginner or seasoned investor, we've got you covered. Start investing smarter today with StockInvestor!.")

# Signup page
elif selected_page == "Signup":
    st.subheader("Signup")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    if st.button("Signup"):
        if new_password == confirm_password:
            # Store user data (Replace with your preferred method)
            user_data[new_username] = {
                "password": new_password,
                "dob": dob,
                "gender": gender
            }
            st.success("Account created for {}".format(new_username))
        else:
            st.error("Passwords do not match")

# Login page
elif selected_page == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in user_data and user_data[username]["password"] == password:
            st.success("Logged in as {}".format(username))
            # Add redirection or further functionality here
        else:
            st.error("Invalid username or password")

# Questionnaire page
elif selected_page == "Questionnaire":
    st.subheader("Questionnaire")
    income = st.number_input("What is your annual income?")
    investment_amount = st.number_input("How much would you like to invest?")
    expected_return = st.selectbox("What is your expected rate of return?", ["<5%", "5-10%", ">10%"])
    if st.button("Submit"):
        st.write("Thank you for providing your information.")
        # Categorize investor based on risk profile
        investor_type = categorize_investor(income, investment_amount, expected_return)
        st.write(f"Based on your inputs, your investor type is: {investor_type}")

# Stock Recommendation page
elif selected_page == "Stock Recommendation":
    st.subheader("Stock Recommendation")
    selected_stock = st.sidebar.selectbox('Select Stock', stock_list)
    if selected_stock:
        company_data = fetch_stock_data(selected_stock)
        if company_data is not None:
            st.subheader(f"Closing Price of {selected_stock}")
            st.line_chart(company_data['Close'])

            # Display volume sales
            st.subheader("Volume Sales")
            st.line_chart(company_data['Volume'])

            # Calculate and display moving average
            period = st.slider("Select Moving Average Period", min_value=5, max_value=50, value=20, step=5)
            company_data['Moving_Average'] = company_data['Close'].rolling(window=period).mean()
            st.subheader(f"Moving Average ({period} days)")
            st.line_chart(company_data['Moving_Average'])


# In[ ]:




