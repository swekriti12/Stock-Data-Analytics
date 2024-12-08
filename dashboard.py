import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import alpha_vantage
from alpha_vantage.fundamentaldata import FundamentalData
import stocknews
from stocknews import StockNews

st.title('Stock Market Analysis Dashboard')
ticker = st.sidebar.text_input('Ticker', 'GOOGL')
start_date = st.sidebar.date_input('Start Date', pd.Timestamp('2023-01-01'))
end_date = st.sidebar.date_input('End Date', pd.Timestamp('2024-01-01'))

if not ticker:
    st.error("Please enter a valid ticker symbol")
else: 
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.error("No data found for the given ticker and date range.")
        st.stop()
    else:
        # Create the plot
        fig = px.line(data, x=data.index, y=data['Adj Close'].values.flatten(), title=f"{ticker} Stock Price")
        
        # Explicitly set the y-axis label to 'Adj Close'
        fig.update_layout(
            yaxis_title='Adj Close'
        )
        
        st.plotly_chart(fig)

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
            #key = 'KMNZTW37RQIUSB1K'
            key = 'IY9P5YA3GKL31DRJ'
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
                st.write(f"Date: {df_news['published'][i]}")
                st.write(f"Summary: {df_news['summary'][i]}")

                # Check if there's a link column and display the link (if available)
                if 'link' in df_news.columns:
                    st.write(f"Link: [Read More]({df_news['link'][i]})")
                else:
                    st.write("Link: Not available")

                # Sentiment analysis output
                title_sentiment = df_news['sentiment_title'][i]
                news_sentiment = df_news['sentiment_summary'][i]
                st.write("Sentiments:")
                st.write(f"Title Sentiment: {title_sentiment}")
                st.write(f"News Sentiment: {news_sentiment}")
