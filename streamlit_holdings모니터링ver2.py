#!/usr/bin/env python
# coding: utf-8


# # 세번째코드 (2024.7.12)

# ## 엑셀 파일 넣기

# In[18]:
import streamlit as st
import pandas as pd
import yfinance as yf

st.title("ETF Holdings 모니터링")

# Create an upload button
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

# In[ ]:
import pandas as pd



# In[ ]:
#if uploaded_file is not None:
#    # Read only column A from the file
#    df = pd.read_excel(uploaded_file, usecols="A")
#    st.write(df)



# In[ ]:
# Initialize a session state for dates if not already initialized
# Initialize a session state for dates if not already initialized
import datetime
import time


# Initialize a session state for dates if not already initialized

# Initialize a session state for dates if not already initialized
if 'dates' not in st.session_state:
    st.session_state.dates = [None, None, None]

# Function to add a new date input
def add_date():
    st.session_state.dates.append(None)

# Function to remove the last date input
def remove_date():
    if len(st.session_state.dates) > 0:
        st.session_state.dates.pop()

# Create the first date input widget for the end date
st.session_state.dates[0] = st.date_input("end date", key="date_input_0", value=datetime.date(2023, 1, 1))

# Create date input widgets for the start dates
for i in range(1, len(st.session_state.dates), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(st.session_state.dates):
            label = f"start date{i + j}" if i + j > 0 else "end date"
            with cols[j]:
                st.session_state.dates[i + j] = st.date_input(label, key=f"date_input_{i + j}", value=datetime.date(2022, 1, 1))

# Display buttons to add or remove date inputs
st.button("Add Date", on_click=add_date)
st.button("Remove Date", on_click=remove_date)

def fetch_ticker_data(ticker):
    retries = 5
    for attempt in range(retries):
        try:
            ticker_data = yf.download(ticker, period='5y')
            return ticker_data
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5)  # Retry after 5 seconds
                continue
            else:
                st.write(f"Error fetching data for {ticker}: {e}")
                return None

def calculate_returns(df, end_date, start_dates):
    for i, ticker in enumerate(df['ticker']):
        st.write(f"Fetching data for {ticker}...")
        ticker_data = fetch_ticker_data(ticker)
        if ticker_data is None:
            continue
        
        st.write(f"Data for {ticker} from yfinance:", ticker_data)
        try:
            end_price = ticker_data.loc[end_date, 'Close']
            st.write(f"End price for {ticker} on {end_date}: {end_price}")
            
            for j, start_date in enumerate(start_dates):
                start_price = ticker_data.loc[start_date, 'Close']
                st.write(f"Start price for {ticker} on {start_date}: {start_price}")
                return_col = f'수익률{j+1}'
                if return_col not in df.columns:
                    df[return_col] = None
                df.loc[i, return_col] = (end_price / start_price - 1) * 100
                st.write(f"Return for {ticker} from {start_date} to {end_date}: {df.loc[i, return_col]}%")
        except KeyError as e:
            st.write(f"Data for {ticker} does not contain the date {e}")
        except Exception as e:
            st.write(f"Error processing data for {ticker}: {e}")
    return df

if uploaded_file is not None:
    # Read the file
    df = pd.read_excel(uploaded_file)

    # Split the first column into 'ticker' and 'Country'
    new_columns = df.iloc[:, 0].str.split(' ', n=1, expand=True)
    new_columns.columns = ['ticker', 'Country']
    
    # Combine the new columns with the rest of the dataframe
    df = pd.concat([new_columns, df.iloc[:, 1:]], axis=1)
    
    # Convert the third and fourth columns to percentages
    if df.shape[1] > 2:
        df.iloc[:, 2] = df.iloc[:, 2].apply(lambda x: f"{x * 100:.2f}%")
    if df.shape[1] > 3:
        df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: f"{x * 100:.2f}%")
    
    # Display the dataframe before calculating returns
    st.write("Uploaded Data:", df)
    
    # Button to calculate returns
    if st.button("Check return rate"):
        # Convert date inputs to strings for compatibility with yfinance
        try:
            end_date = st.session_state.dates[0].strftime('%Y-%m-%d')
            start_dates = [date.strftime('%Y-%m-%d') for date in st.session_state.dates[1:] if date is not None]
        
            # Calculate returns and update the dataframe
            df = calculate_returns(df, end_date, start_dates)
        
            # Format the returns columns as percentages
            for col in df.columns:
                if '수익률' in col:
                    df[col] = df[col].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else None)
        
            # Display the modified dataframe
            st.write("Data with Returns:", df)
        except Exception as e:
            st.write(f"Error during return calculation: {e}")








# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




