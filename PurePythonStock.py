import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import tkinter as tk
from tkinter import *
def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)

def GUIDisplay():
    global display
    display = tk.Tk()
    AskForCompany = tk.Label(text='What Company Would You Like To Look At?')
    AskForCompany.pack()
    global GETCompanyName
    GETCompanyName = tk.Entry()
    GETCompanyName.pack()
    B = tk.Button(display, text = "OK", command = get_company_name)
    B.pack()
    display.mainloop()

def generate_filename(search_term):
    stem = path = '_'.join(search_term.split(' '))
    global filename
    filename = stem + '.csv'
    return filename

def get_company_name():
    global CompanyName
    CompanyName = GETCompanyName.get()
    generate_filename(CompanyName)
    global data 
    #FIX THIS INTERVAL AND PERIOD
    data = yf.download(CompanyName, period = "1mo", interval = "1d")
    makeGraph()

def makeGraph():
    #declare figure
    global fig
    fig = go.Figure()
    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'], name = 'market data'))
    # Add titles
    DataTitle = 'STOCK for: ' + CompanyName
    fig.update_layout(
        title=DataTitle,
        yaxis_title='Stock Price (USD per Shares)')
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def DisplayResultsOnGUI():
    global DisplayResult
    DisplayResult = tk.Tk()
    DisplayResult.geometry("1000x1000")
    text = Text(DisplayResult)
    text.insert(INSERT, "Here Are Your Results: \n")
    global COMPANY
    COMPANY = yf.Ticker(CompanyName)
    global history
    history = COMPANY.history(period="max")
    text.insert(INSERT, history)
    text.insert(INSERT, "\n")

    global info
    info = COMPANY.info
    text.insert(INSERT,info)
    text.insert(INSERT, "\n")

    global actions
    actions = COMPANY.actions 
    text.insert(INSERT,actions)
    text.insert(INSERT, "\n")

    global currentStockPrice 
    currentStockPrice = get_current_price(CompanyName) 
    text.insert(INSERT, currentStockPrice)
    text.insert(INSERT, "\n")

    text.pack(expand=True, fill=BOTH)
    text.insert(INSERT, "Do You Want to Store the Data In a TXT File?")
    YesButton = tk.Button(DisplayResult, text = "YES", command = StoreInTXT).pack()
    CloseGUI = tk.Button(DisplayResult, text = "Close This GUI", command = DisplayResult.destroy).pack()
    DisplayResult.mainloop()
#write into txt or  csv file
def StoreInTXT():
    f = open(filename, "a")
    f.write(str(history) + "\n")
    f.write(str(info) + "\n")
    f.write(str(actions) + "\n")
    f.write(str(currentStockPrice) + "\n")
    f.close()

GUIDisplay()
DisplayResultsOnGUI()