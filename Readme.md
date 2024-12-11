## Stock Market Dashboard with Streamlit

This Stock Market Dashboard is a Streamlit application that allows users to analyze various aspects of publicly traded companies.

### Features

* **Stock Price Analysis:** 
    * Select a ticker symbol from the S&P 500 list or enter a custom ticker.
    * Choose a date range to view historical stock price data.
    * Visualize the stock price trend using a line chart.
    * Calculate and display key metrics like annual return, standard deviation, and risk-adjusted return.
* **Fundamental Data Exploration:**
    * Access fundamental data for the selected company, including:
        * Market capitalization
        * Price-to-earnings (P/E) ratio
        * Earnings per share (EPS)
        * Dividend yield
* **Financial Statement Breakdown:**
    * Deep dive into the company's financial health by exploring:
        * Balance sheet
        * Income statement
        * Cash flow statement
* **News and Sentiment Analysis:**
    * Get a snapshot of the latest news headlines related to the chosen stock.
    * Analyze the sentiment (positive, negative, or neutral) of both the news titles and summaries.

### Technologies Used

* Streamlit: Web framework for building data apps.
* Pandas: Data manipulation library.
* yfinance: Python library for downloading financial data.
* Plotly: Interactive visualization library.
* datetime: Python module for handling date and time objects.
* alpha_vantage: Python library for accessing financial data from Alpha Vantage API.
* stocknews: Python library for fetching news articles related to stocks.

### How to Run
#### Use python version 3.11.10

1. Clone or download this repository.
[https://github.com/swekriti12/Stock-Data-Analytics](https://github.com/swekriti12/Stock-Data-Analytics)

2. Navigate to the project directory in your terminal.

3. Install the required libraries:

```bash
pip install -r requirement.txt
```
4. Run the application:

```bash
streamlit run dashboard.py
```

4. You can see the terminal displays like this where you can access the dashboard:

```bash
  Local URL: http://localhost:8501
  Network URL: http://10.0.0.39:8501
```

**Note:** This application requires an Alpha Vantage API key to access financial data. You can obtain a free API key from [https://www.alphavantage.co/](https://www.alphavantage.co/). Store your API key in a secure environment variable and reference it within the code.

### Code Breakdown

The code utilizes Streamlit to create a user-friendly interface with various functionalities. Here's a high-level overview of the key functionalities:

* **`get_sp500_tickers` function:** Retrieves a list of S&P 500 tickers dynamically from Wikipedia.
* **`classify_sentiment` function:** Analyzes sentiment based on a sentiment ratio threshold, classifying it as positive, negative, or neutral.
* **Data retrieval and visualization:**
    * Historical stock price data is downloaded using `yf.download`.
    * Line charts are created using `px.line` with customized formatting.
    * Key financial metrics and financial statements are retrieved using Alpha Vantage API.
* **News and sentiment analysis:**
    * Top news articles are fetched using `StockNews`.
    * Sentiment analysis is performed on news titles and summaries.


This is a basic overview of the code functionalities. Refer to the code itself (`dashbboard.py`) for detailed implementation.

### Further Customization

This dashboard offers a foundation for analyzing stock market data. We can further enhance it by:

* Adding more financial metrics and calculations.
* Implementing additional technical analysis indicators.
* Integrating with other financial data sources.
* Enhancing the news and sentiment analysis functionalities to predict the price.
* We can implement virtual assistant augmented with the retrieved data for further Q/A.
