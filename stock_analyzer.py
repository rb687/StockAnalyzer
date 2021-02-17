#!/usr/bin/env python


import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

headings = ("Stock", "Symbol", "PE")
data = ()

"""

Sample data: 

Ticker, 
current price, 
PE ratio, 
PE ratio of industry, 
P/B ratio, 
EPS(TTM), 
Ex-Dividend Date, 
Dividend Yield 
1y Target estimate, 
52 week range, 
5 year range, 
day range, 
Graham method fair value, 

"""

STOCK_SYMBOL = {
    "MSFT": "Microsoft",
    "NOW": "Service Now",
    "APPL": "Apple Inc."
}


class Stock:
    def __init__(self, ticker, name, pe=None, pb=None, eps=None,
               dividend_yield=0, eoy_target=None, graham_fair_value=None):
        self.ticker = ticker
        self.name = name
        self.pe = pe
        self.pb = pb
        self.eps = eps
        if dividend_yield != None:
            self.dividend_yield = dividend_yield * 100
        else:
            self.dividend_yield = 0
        # 1 year estimated price
        self.eoy_target = eoy_target
        # 52 week range
        self.graham_fair_value = graham_fair_value
        self.growth_rate = 0
        self.risk_free_rate = 0.07  # India's 7% from FD

    def calc_graham_fair_value(self):
        val = (self.eps * (8.5 + 2 * self.growth_rate) * 4.4) / self.risk_free_rate
        self.graham_fair_value = val

    def serialize(self):
        return self.__dict__


@app.route('/health')
def health_check():
    return "Stock analyzer is running!"


@app.route('/')
def display_all():
    headings = ("Symbol", "Name", "Trailing PE", "Book Value", "Trailing EPS", "Dividend Yield")
    data = []
    cols = []

    for symbol in STOCK_SYMBOL:
        print symbol
        tkr_details = yf.Ticker(symbol).info
        stock = Stock(ticker=symbol, name=STOCK_SYMBOL[symbol], pe=tkr_details.get("trailingPE"),
                      pb=tkr_details.get("bookValue"),
                      eps=tkr_details.get("trailingEps"), dividend_yield=tkr_details.get("dividendYield"),
                      eoy_target=None, graham_fair_value=None)
        data.append(stock.serialize())
        cols = stock.serialize().keys()
    return render_template("table.html", data=data, headings=cols)


'''
@app.route('/<ticker>')
def pull_data(ticker):
    print "Pulling data for ticket {}!".format(ticker)
    ticker_details = yf.Ticker(ticker)
    day_range = ticker_details.get("dayLow") + " - " + ticker_details.get("dayHigh")
    year_range = ticker_details.get("fiftyTwoWeekHigh") + " - " + ticker_details.get("fiftyTwoWeekLow")
    stock1 = Stock(ticker_details.get("symbol"),
                        ticker_details.get("trailingPE"),
                        ticker_details.get("priceToBook"),
                        ticker_details.get("trailingEps"),
                        ticker_details.get("exDividendDate"),
                        ticker_details.get("dividendYield"),
                        ticker_details.get("eoy_target"), 
                        ticker_details.get(year_range),
                        ticker_details.get(day_range)
        )

'''

if __name__ == '__main__':
    app.run(port=1111)
