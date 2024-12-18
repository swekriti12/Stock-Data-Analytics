#Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import datetime
import alpha_vantage
from alpha_vantage.fundamentaldata import FundamentalData
import stocknews
from stocknews import StockNews

with open("./streamlit.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Function to get S&P 500 tickers dynamically
def get_sp500_tickers():
    #Use Wikipedia's S&P 500 list to fetch tickers
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0]
    #Extract the tickers from the 'Symbol' column
    tickers = df['Symbol'].tolist()  
    return tickers

neutral_threshold = 0.1  # Adjust this as per your use case

# Function to determine sentiment
def classify_sentiment(ratio):
    if ratio > 0.5 + neutral_threshold:
        return "Positive"
    elif ratio < 0.5 - neutral_threshold:
        return "Negative"
    else:
        return "Neutral"

#Get the list of all tickers
tickers_list = get_sp500_tickers()

#Set title for the dashboard
st.title('Stock Market Dashboard')

#Create a dropdown menu with a search bar to allow users to select a ticker or enter a custom ticker
ticker = st.sidebar.selectbox('Select Ticker', tickers_list + ['Other'], key="ticker_dropdown", index=tickers_list.index('GOOGL') if 'GOOGL' in tickers_list else 0)

#If 'Other' is selected, allow user to enter a custom ticker
if ticker == 'Other':
    ticker = st.sidebar.text_input('Enter Ticker Symbol', 'GOOGL')

#Get today's date for the end date
end_date_default = datetime.datetime.today().date()

#Set the default start date to be 365 days before the end date
start_date_default = end_date_default - datetime.timedelta(days=365)

#Create the date input for the end date and start date, with max_date set to today
start_date = st.sidebar.date_input('Start Date', start_date_default, max_value=end_date_default)
end_date = st.sidebar.date_input('End Date', end_date_default, max_value=end_date_default)

#Update start_date if end_date changes
if start_date > end_date:
    st.sidebar.error("Start Date must be earlier than End Date!")
    start_date = end_date - datetime.timedelta(days=365)

# Add the group name and student names to the sidebar
st.sidebar.markdown(f"""
<div class="group-name">
<span> Created by Big Data Analytics Students: </span>
<span> Anish Saini, Ashish Thapa, Manushi Khadka, Siddhant Praveen Kapse, Swekriti Poudel </span>
</div>
""", 
unsafe_allow_html=True)

#If the ticket has not been selected or input provide a error message
if not ticker:
    st.error("Please enter a valid ticker symbol")
       
else: 
    data = yf.download(ticker, start=start_date, end=end_date)
    #If there is not data for the selected ticker or the selected date range
    if data.empty:
        st.error("No data found for the given ticker and date range.")
        st.stop()
        
    else:
        #Create the plot
        fig = px.line(data, x=data.index, y=data['Adj Close'].values.flatten(), title=f"{ticker} Stock Price")
        
        #Explicitly set the y-axis label to 'Adj Close'
        fig.update_layout(
            yaxis_title='Adj Close'
        )
        
        #Update hover data to show the correct label
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Adj Close: %{y}<extra></extra>'  # Customize hover text
        )
        
        st.plotly_chart(fig, key=f"{ticker}_plot")
        

        pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "News"])

        with pricing_data:
            st.header('Price Movement')
    
            if not data.empty:
                #Create a copy to avoid modifying the original data
                data2 = data.copy()
                
                #Calculate percent change
                data2['% Change'] = (data['Adj Close'] / data['Adj Close'].shift(1) - 1) * 100
                
                #Drop missing values created by shift
                data2.dropna(inplace=True)
                 
                # Clean up any tuple column names (e.g., '% Change' and empty string)
                data2.columns = [col[0] if isinstance(col, tuple) else col for col in data2.columns]
                       
                #Display the data with the % Change column  
                st.write(data2)
        
                annual_return = data2['% Change'].mean() * 252
                st.write(f'Annual return is {annual_return:.2f}%')
        
                stdev = np.std(data2['% Change']) * np.sqrt(252)
                st.write(f'Standard Deviation is {stdev:.2f}%')
        
                risk_adj_return = annual_return / stdev
                st.write(f'Risk Adjusted Return is {risk_adj_return:.2f}')
        
            else:
                st.warning("No pricing data available.")


        with fundamental_data:
            def get_fundamental_data(ticker):
                stock = yf.Ticker(ticker)
                info = stock.info
                market_cap = info.get('marketCap', 'N/A')
                pe_ratio = info.get('trailingPE', 'N/A')
                eps = info.get('trailingEps', 'N/A')
                dividend_yield = info.get('dividendYield', 'N/A')
                return market_cap, pe_ratio, eps, dividend_yield

            with fundamental_data:
                st.subheader('Key Metrics')
                market_cap, pe_ratio, eps, dividend_yield = get_fundamental_data(ticker)
                st.write(f"**Market Cap**: {market_cap}")
                st.write(f"**P/E Ratio**: {pe_ratio}")
                st.write(f"**EPS**: {eps}")
                st.write(f"**Dividend Yield**: {dividend_yield}")
            
            
            # key = 'KMNZTW37RQIUSB1K'
            # key = 'IY9P5YA3GKL31DRJ'
            key = 'Y1XI5SU13KB3VK8H'
            fd = FundamentalData(key, output_format = 'pandas')

            st.subheader('Balance Sheet')
            balance_sheet = fd.get_balance_sheet_annual(ticker[0])[0]  # Get the DataFrame from the tuple
            bs = balance_sheet.T[2:]  # Transpose the DataFrame
            bs.columns = list(balance_sheet.T.iloc[0])  # Set the new column names
            bs.index = bs.index.str.replace('([a-z])([A-Z])', r'\1 \2', regex=True).str.title()
            st.write(bs)

            st.subheader('Income Statement')
            income_statement = fd.get_income_statement_annual(ticker)[0]  # Get the DataFrame from the tuple
            is1 = income_statement.T[2:]  # Transpose the DataFrame
            is1.columns = list(income_statement.T.iloc[0])  # Set the new column names
            is1.index = is1.index.str.replace('([a-z])([A-Z])', r'\1 \2', regex=True).str.title()
            st.write(is1)

            st.subheader('Cash Flow Statement')
            cash_flow = fd.get_cash_flow_annual(ticker)[0]  # Get the DataFrame from the tuple
            cf = cash_flow.T[2:]  # Transpose the DataFrame
            cf.columns = list(cash_flow.T.iloc[0])  # Set the new column names
            cf.index = cf.index.str.replace('([a-z])([A-Z])', r'\1 \2', regex=True).str.title()
            st.write(cf)

        
        with news:
            st.header(f'Top 5 News for {ticker}')
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()
    
            for i in range(5):
                st.subheader(f"{i + 1}. {df_news['title'][i]}")
                date_obj = datetime.datetime.strptime(df_news['published'][i], "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_obj.strftime("%a, %d %b %Y")
                st.write(f"Date: {formatted_date}")
                st.write(f"Summary: {df_news['summary'][i]}")

                # Sentiment analysis output
                title_sentiment = df_news['sentiment_title'][i]
                news_sentiment = df_news['sentiment_summary'][i]
                st.write(f"Title Sentiment: {classify_sentiment(title_sentiment)}")
                st.write(f"News Sentiment: {classify_sentiment(news_sentiment)}")
