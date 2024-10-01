import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

import pandas as pd
import numpy as np

import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mplfinance
from mplfinance.original_flavor import candlestick_ohlc
import plotly.graph_objects as go

from tvDatafeed import TvDatafeed, Interval

requiredInterval = Interval.in_daily


largeFont = ("Verdana", 15)
bulletFont = ("Verdana", 13)
normFont = ("Verdana", 10)
smallFont = ("Verdana", 8)

style.use("ggplot")

f = plt.figure()
#plt.ion()
#a =  f.add_subplot(111)
a0 = None
a = None
a2 = None
a3  = None

price_counter = 9000
indicator_counter = 9000

requiredExchange = "COINBASE"
programName = "NSE"
firstTime = True

topIndicator = "none"
midIndicator = "none"
bottomIndicator = "none"

price_need_to_be_updated =  True
indicator_need_to_be_updated = False


SMAs = []
EMAs = []

stock_list = [
    "BTCUSD",
    "ETHUSD",
    "XRPUSD"
]


chartLoad = False


def searchFunction():

    midIQ = tk.Tk()
    midIQ.wm_title("Search")
    label = ttk.Label(midIQ, text = "Cryptocurrency: ")
    label.pack(side = "top", fill = "x", pady = 10)

    e = ttk.Entry(midIQ)
    e.insert(0, "")
    e.pack()
    e.focus_set()

    label2 = ttk.Label(midIQ, text = "Exchange: ")
    label2.pack(side = "top", fill = "x", pady = 10)

    e2 = ttk.Entry(midIQ)
    e2.insert(0, "")
    e2.pack()
    e2.focus_set()

    def callback():
        global requiredExchange
        global stock_to_plot
        global price_need_to_be_updated
        global indicator_need_to_be_updated
        tv = TvDatafeed()
        midIndicator = []
        crypto = (e.get())
        exchange = (e2.get())
        
        try_searched = tv.get_hist(symbol=crypto,exchange=exchange,interval=requiredInterval,n_bars=1)
        if type(try_searched) == pd.DataFrame:
            requiredExchange = exchange
            stock_to_plot = crypto
            global firstTime
            firstTime = True
            price_need_to_be_updated = True
            indicator_need_to_be_updated = True
            
        else: 
            error = tk.Tk()
            error.wm_title("Error")
            label = ttk.Label(error, text = '''The combination of cryptocurrency and exchange selected does not exist.
            Please make sure to not make any typos.''')
            label.pack(side = "top", fill = "x", pady = 10)
        '''group = []
        group.append("sma")
        group.append(int(length))
        midIndicator.append(group)
        print("midIndicator set to: ", midIndicator)'''
        midIQ.destroy()

    button = ttk.Button(midIQ, text = "Submit", width = 10, command = callback)
    button.pack()

    tk.mainloop()


def changeStock(*args):
    global price_need_to_be_updated
    global indicator_need_to_be_updated
    global firstTime
    global chartLoad
    global stock_to_plot
    stock_to_plot = args[0]
    chartLoad = True
    firstTime = True
    price_need_to_be_updated = True
    indicator_need_to_be_updated = True

def normalize(series):
    max_val = series.max()
    
    # Apply rescaling to each value in the Series
    scaled_series = series.apply(lambda x: max_val * 0.05 if x < max_val * 0.05 else x)
    
    return scaled_series
    

def loadChart(todo):
    global chartLoad
    if (todo == "start"):
        chartLoad = True
    elif (todo == "stop"):
        chartLoad = False


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    fast_ema = data.ewm(span = fast_period, min_periods = fast_period).mean()
    slow_ema = data.ewm(span = slow_period, min_periods = slow_period).mean()
    
    macd_line = fast_ema - slow_ema      
    signal_line = macd_line.ewm(span = signal_period, min_periods = signal_period).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def tutorial():
    print("hello")
    def page2():
        tut.destroy()
        tut2 = tk.Tk()
        
        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title("Part 3!")
            label = ttk.Label(tut3, text = "Part 3", font = normFont)
            label.pack(side = "top", pady = 10, fill = "x")

            button1 = ttk.Button(tut3, text = "Done!", command = tut3.destroy)
            button1.pack()
            tut3.mainloop

        tut2.wm_title("Part 2!")
        label = ttk.Label(tut2, text = "Part 2", font = normFont)
        label.pack(side = "top", pady = 10, fill = "x")

        button1 = ttk.Button(tut2, text = "Next", command = page3)
        button1.pack()
        tut2.mainloop

    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label = ttk.Label(tut, text = "What do you need help with?", font = normFont)
    label.pack(side = "top", pady = 10, fill = "x")

    button1 = ttk.Button(tut, text = "Overview of application", command = page2)
    button1.pack()

    button2 = ttk.Button(tut, text = "How do I trade with this client?", command = lambda: popupmsg("Not yet completed"))
    button2.pack()

    button3 = ttk.Button(tut, text = "Overview of application", command = lambda: popupmsg("Not yet completed"))
    button3.pack()   
    print("eh")
    tut.mainloop()

def changeTopIndicator(requiredIndicator):
    global topIndicator
    
    global indicator_need_to_be_updated
    indicator_need_to_be_updated = True
    
    global price_need_to_be_updated
    price_need_to_be_updated = True

    global top_rsi_was_updated_and_hence_price_needs_update
    global top_rsi_was_updated_and_hence_indicator_needs_update

    if (requiredIndicator == "none"):
        topIndicator = requiredIndicator
    elif (requiredIndicator == "rsi"):
        top_rsi_was_updated_and_hence_price_needs_update = True
        top_rsi_was_updated_and_hence_indicator_needs_update = True
        rsiQ = tk.Tk()
        rsiQ.wm_title("RSI Length")
        label = ttk.Label(rsiQ, text = "Enter RSI Length")
        label.pack(side = "top", pady = 10, fill = "x")
        
        e = ttk.Entry(rsiQ, width = 15)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            length = (e.get())
            group = []
            group.append("rsi")
            group.append(length)
            topIndicator = group
            print("Set top indicator to" + str(topIndicator))
            rsiQ.destroy()
        
        button = ttk.Button(rsiQ, text = "Submit", width = 10, command = callback)
        button.pack()
        tk.mainloop()

    elif (requiredIndicator == "macd"):
        topIndicator = requiredIndicator

def changeBottomIndicator(requiredIndicator):
    global bottomIndicator
    global bottom_rsi_was_updated_and_hence_price_needs_update
    global bottom_rsi_was_updated_and_hence_indicator_needs_update
    
    global price_need_to_be_updated
    price_need_to_be_updated = True
            
    global indicator_need_to_be_updated
    indicator_need_to_be_updated = True

    
    if (requiredIndicator == "none"):
        bottomIndicator = requiredIndicator
    elif (requiredIndicator == "rsi"):
        bottom_rsi_was_updated_and_hence_price_needs_update = True
        bottom_rsi_was_updated_and_hence_indicator_needs_update = True
        rsiQ = tk.Tk()
        rsiQ.wm_title("RSI Length")
        label = ttk.Label(rsiQ, text = "Enter RSI Length")
        label.pack(side = "top", pady = 10, fill = "x")
        
        e = ttk.Entry(rsiQ, width = 15)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            length = (e.get())
            group = []
            group.append("rsi")
            group.append(length)
            bottomIndicator = group
            print("Set bottom indicator to" + str(bottomIndicator))
            rsiQ.destroy()
        button = ttk.Button(rsiQ, text = "Submit", width = 10, command = callback)
        button.pack()
        tk.mainloop()

    elif (requiredIndicator == "macd"):
        bottomIndicator = requiredIndicator


   

def changeMidIndicator(requiredIndicator):
    global midIndicator
    global price_need_to_be_updated
    global indicator_need_to_be_updated
    global midIndicator_was_updated
    
    global midIndicator_was_updated_and_hence_price_needs_update
    global midIndicator_was_updated_and_hence_indicator_needs_update

    '''midIndicator_was_updated_and_hence_price_needs_update = True
    midIndicator_was_updated_and_hence_indicator_needs_update = True'''
    
    if (requiredIndicator != "none"):
        if (midIndicator == "none"):
            if (requiredIndicator == "sma"):
                midIQ = tk.Tk()
                midIQ.wm_title("SMA length")
                label = ttk.Label(midIQ, text = "Enter length of SMA")
                label.pack(side = "top", fill = "x", pady = 10)

                e = ttk.Entry(midIQ)
                e.insert(0, 9)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator_was_updated_and_hence_price_needs_update
                    global midIndicator_was_updated_and_hence_indicator_needs_update
                    global midIndicator
                    midIndicator = []
                    length = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(length))
                    midIndicator.append(group)
                    midIndicator_was_updated_and_hence_price_needs_update = True
                    midIndicator_was_updated_and_hence_indicator_needs_update = True
                    print("midIndicator set to: ", midIndicator)
                    midIQ.destroy()
                    

                button = ttk.Button(midIQ, text = "Submit", width = 10, command = callback)
                button.pack()
                tk.mainloop()

            if (requiredIndicator == "ema"):
                midIQ = tk.Tk()
                midIQ.wm_title("EMA length")
                label = ttk.Label(midIQ, text = "Enter length of EMA")
                label.pack(side = "top", fill = "x", pady = 10)

                e = ttk.Entry(midIQ)
                e.insert(0, 9)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator_was_updated_and_hence_price_needs_update
                    global midIndicator_was_updated_and_hence_indicator_needs_update
                    global midIndicator
                    midIndicator = []
                    length = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(length))
                    midIndicator.append(group)
                    midIndicator_was_updated_and_hence_price_needs_update = True
                    midIndicator_was_updated_and_hence_indicator_needs_update = True
                    print("midIndicator set to: ", midIndicator)
                    midIQ.destroy()
                    

                button = ttk.Button(midIQ, text = "Submit", width = 10, command = callback)
                button.pack()
                tk.mainloop()

        else:
            if (requiredIndicator == "sma"):
                midIQ = tk.Tk()
                midIQ.wm_title("SMA length")
                label = ttk.Label(midIQ, text = "Enter length of SMA")
                label.pack(side = "top", fill = "x", pady = 10)

                e = ttk.Entry(midIQ)
                e.insert(0, 9)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator_was_updated_and_hence_price_needs_update
                    global midIndicator_was_updated_and_hence_indicator_needs_update
                    global midIndicator
                    length = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(length))
                    midIndicator.append(group)
                    midIndicator_was_updated_and_hence_price_needs_update = True
                    midIndicator_was_updated_and_hence_indicator_needs_update = True
                    print("midIndicator set to: ", midIndicator)
                    midIQ.destroy()
                    

                button = ttk.Button(midIQ, text = "Submit", width = 10, command = callback)
                button.pack()
                tk.mainloop()

            if (requiredIndicator == "ema"):
                midIQ = tk.Tk()
                midIQ.wm_title("EMA length")
                label = ttk.Label(midIQ, text = "Enter length of EMA")
                label.pack(side = "top", fill = "x", pady = 10)

                e = ttk.Entry(midIQ)
                e.insert(0, 9)
                e.pack()
                e.focus_set()

                def callback():
                    global midIndicator_was_updated_and_hence_price_needs_update
                    global midIndicator_was_updated_and_hence_indicator_needs_update
                    global midIndicator
                    #midIndicator = []
                    length = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(length))
                    midIndicator.append(group)
                    midIndicator_was_updated_and_hence_price_needs_update = True
                    midIndicator_was_updated_and_hence_indicator_needs_update = True
                    print("midIndicator set to: ", midIndicator)
                    midIQ.destroy()
                    

                button = ttk.Button(midIQ, text = "Submit", width = 10, command = callback)
                button.pack()
                
                tk.mainloop()

    else:
        midIndicator = "none"
        global midIndicator_was_updated_and_hence_price_needs_update
        global midIndicator_was_updated_and_hence_indicator_needs_update
        midIndicator_was_updated_and_hence_price_needs_update = True
        midIndicator_was_updated_and_hence_indicator_needs_update = True

def changeExchange(toWhat):
    global requiredExchange
    global programName
    global firstTime
    requiredExchange = toWhat
    firstTime = True
    
    global price_need_to_be_updated 
    global indicator_need_to_be_updated
    price_need_to_be_updated = True
    indicator_need_to_be_updated = True


def changeTimeframe(timeframe):
    global requiredInterval
    global firstTime
    
    global price_need_to_be_updated 
    global indicator_need_to_be_updated
    price_need_to_be_updated = True
    indicator_need_to_be_updated = True
    
    firstTime = True

    if timeframe == "1d":
        requiredInterval = Interval.in_daily
    elif timeframe == "1h":
        requiredInterval = Interval.in_1_hour
    elif timeframe == "1min":
        requiredInterval = Interval.in_1_minute
    elif timeframe == "5min":
        requiredInterval = Interval.in_5_minute
    elif timeframe == "15min":
        requiredInterval = Interval.in_15_minute
    elif timeframe == "4h":
        requiredInterval = Interval.in_4_hour
    elif timeframe == "1w":
        requiredInterval = Interval.in_weekly
    elif timeframe == "1mon":
        requiredInterval = Interval.in_monthly
    print(price_need_to_be_updated)
        
def popupmsg(msg):
    popup = tk.Tk()
        
    popup.wm_title("Error!")
    label = ttk.Label(popup, text = msg, font = normFont)
    label.pack(side = "top", fill = "x", pady = 10)

    button1 = ttk.Button(popup, text = "Ok", command = popup.destroy)
    button1.pack()
    popup.mainloop()

nifty = pd.DataFrame()
data = None
volume = None
allDates = None

midIndicator_was_updated_and_hence_price_needs_update = False
midIndicator_was_updated_and_hence_indicator_needs_update = False

top_rsi_was_updated_and_hence_price_needs_update = False
top_rsi_was_updated_and_hence_indicator_needs_update = False

bottom_rsi_was_updated_and_hence_price_needs_update = False
bottom_rsi_was_updated_and_hence_indicator_needs_update = False


def animate(i):
    global price_counter
    global indicator_counter
    global data  
    global volume
    global allDates 
    global a0
    global a
    global a2
    global a3
    global price_need_to_be_updated
    global indicator_need_to_be_updated
    global midIndicator_was_updated_and_hence_price_needs_update
    global midIndicator_was_updated_and_hence_indicator_needs_update
    global top_rsi_was_updated_and_hence_price_needs_update
    global top_rsi_was_updated_and_hence_indicator_needs_update
    global bottom_rsi_was_updated_and_hence_price_needs_update
    global bottom_rsi_was_updated_and_hence_indicator_needs_update

    
    if chartLoad: 
        price_counter = price_counter + 1
        indicator_counter = indicator_counter + 1
        global firstTime
        global nifty
        tv = TvDatafeed()
        #nifty_hourly = tv.get_hist(symbol='BTCUSD',exchange='BITSTAMP',interval=Interval.in_1_hour,n_bars=60)
        price_update_over_user_changes = bottom_rsi_was_updated_and_hence_indicator_needs_update or price_need_to_be_updated or midIndicator_was_updated_and_hence_price_needs_update or top_rsi_was_updated_and_hence_price_needs_update
        if (price_update_over_user_changes or (price_counter > 40)):
            if (firstTime): 
                while(firstTime):
                    nifty = tv.get_hist(symbol=stock_to_plot,exchange=requiredExchange,interval=requiredInterval,n_bars=120)
                    if(type(nifty) == pd.DataFrame):
                        firstTime = False
                        break
                
                
            else:
                new_nifty = tv.get_hist(symbol=stock_to_plot,exchange=requiredExchange,interval=requiredInterval,n_bars=1)
                
                if (type(new_nifty) == pd.DataFrame): 
                    if new_nifty.index[0] == nifty.index[-1]:
                        nifty = nifty.drop(nifty.index[-1])
                        nifty = pd.concat([nifty, new_nifty])
                    else:
                        nifty = pd.concat([nifty, new_nifty])
    
            
            plt.clf()
            if bottomIndicator == "none" and topIndicator == "none":
                a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                a.clear()
                print("no indicator set")
                # Volume
                a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)
                a2.clear()
            elif bottomIndicator != "none" and topIndicator == "none":
                a = plt.subplot2grid((6,4), (0,0), rowspan = 4, colspan = 4)
                a.clear()
                print("bottom indicator set")
                # Volume
                a2 = plt.subplot2grid((6,4), (4,0), rowspan = 1, colspan = 4, sharex = a)
                a2.clear()
            elif bottomIndicator == "none" and topIndicator != "none":
                print(topIndicator)
                # Main Graph
                a = plt.subplot2grid((6,4), (1,0), rowspan = 4, colspan = 4)
                a.clear()
                print("top indicator set")
                # Volume
                a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)
                a2.clear()
            elif bottomIndicator != "none" and topIndicator != "none":
                # Main Graph
                a = plt.subplot2grid((6,4), (1,0), rowspan = 3, colspan = 4)
                a.clear()
                print("both indicators set")
                # Volume
                a2 = plt.subplot2grid((6,4), (4,0), rowspan = 1, colspan = 4, sharex = a)
                a2.clear()
                
            allDates = np.array([nifty.index]).astype("datetime64[s]")
            allDates  = allDates.flatten()
            volume  = nifty["volume"]
            data = nifty
            data = data.reset_index(drop = False)
            data["open"] = data["open"].astype("float64")
            data["high"] = data["high"].astype("float64")
            data["low"] = data["low"].astype("float64")
            data["close"] = data["close"].astype("float64")
            data["volume"] = data["volume"].astype("float64")
            data["datetimeCopy"] = data["datetime"]
            data["datetime"] = data["datetimeCopy"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

            if (requiredInterval == Interval.in_1_minute):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.0002, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_5_minute):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.001, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_15_minute):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.003, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_1_hour):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.012, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_4_hour):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.048, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_daily):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 0.288, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_weekly):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 2.016, colorup = "#089981", colordown = "#F23645")
            elif (requiredInterval == Interval.in_monthly):
                csticks = candlestick_ohlc(a, data[["datetime", "open", "high", "low", "close"]].values, width = 8.064, colorup = "#089981", colordown = "#F23645")
            
        
            '''volume = np.where((volume > 0) & (volume <= 0.1), 0.35,
                  np.where((volume > 0.1) & (volume <= 0.2), 0.42,
                  np.where((volume > 0.2) & (volume <= 0.3), 0.47, volume)))'''
            
            volume = normalize(volume)
            volume_color = np.where((nifty["open"]-nifty["close"] > 0), "#F7A9A7", "#92D2CC")
            
            if requiredInterval == Interval.in_1_minute:
                volume_bar_width = 1/(60*24)
            elif (requiredInterval == Interval.in_5_minute):
                volume_bar_width = 1/288
            elif (requiredInterval == Interval.in_15_minute):
                volume_bar_width = 1/96
            elif requiredInterval == Interval.in_1_hour:
                volume_bar_width = 1/24
            elif requiredInterval == Interval.in_4_hour:
                volume_bar_width = 1/6
            elif requiredInterval == Interval.in_daily:
                volume_bar_width = 1
            elif requiredInterval == Interval.in_weekly:
                volume_bar_width = 7
            elif requiredInterval == Interval.in_monthly:
                volume_bar_width = 28
    
            
            a.set_ylabel("Price")
            a2.bar(data["datetime"].values, volume, width = volume_bar_width, color = volume_color, edgecolor = "#E5E5E5")
            a2.set_ylabel("Volume")
            a.xaxis.set_major_locator(mticker.MaxNLocator(7))
            plt.setp(a.get_xticklabels(), visible = False)
            a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        
            price_need_to_be_updated = False
            price_counter = 0


        indicator_update_over_user_changes = bottom_rsi_was_updated_and_hence_indicator_needs_update or indicator_need_to_be_updated or midIndicator_was_updated_and_hence_indicator_needs_update or top_rsi_was_updated_and_hence_indicator_needs_update
        
        if (indicator_update_over_user_changes or indicator_counter > 40):
            if (topIndicator != "none" and bottomIndicator != "none"):
                # Bottom Indicator
                a3 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)
                a3.clear()
                if(bottomIndicator[0] == "rsi"):
                    a3.set_ylim(0,100)
                
                # Top Indicator
                a0 = plt.subplot2grid((6,4), (0,0), rowspan = 1, colspan = 4, sharex = a)
                a0.clear()
                if(topIndicator[0] == "rsi"):
                    a0.set_ylim(0,100)
                
            elif (topIndicator != "none" and bottomIndicator == "none"):
                # Top Indicator
                a0 = plt.subplot2grid((6,4), (0,0), rowspan = 1, colspan = 4, sharex = a)
                a0.clear()
                if(topIndicator[0] == "rsi"):
                    a0.set_ylim(0,100)
        
            elif (topIndicator == "none" and bottomIndicator != "none"):
                # Bottom Indicator
                a3 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)
                a3.clear()
                if(bottomIndicator[0] == "rsi"):
                    a3.set_ylim(0,100)

            if (midIndicator != "none"):
                for eachMA in midIndicator: 
                    if eachMA[0] == "sma":
                        sma = nifty["close"].rolling(window=eachMA[1]).mean()
                        label = str(eachMA[1]) + " SMA" 
                        a.plot(allDates, sma, label = label)
                    if eachMA[0] == "ema":
                        ewma =  nifty["close"].ewm(span = eachMA[1], min_periods = eachMA[1]).mean()
                        label = str(eachMA[1]) + " EMA" 
                        a.plot(allDates, ewma, label = label)
                    a.legend(loc = 0)
                midIndicator_was_updated_and_hence_indicator_needs_update = False
                midIndicator_was_updated_and_hence_price_needs_update = False
        
            def calculateRSI(prices, period=14):
                period = int(period)
                if len(prices) <= period:
                    return [None] * len(prices)  # Return None for each value if not enough data
            
                deltas = np.diff(prices)
                seed = deltas[:period]
                up = np.maximum(seed, 0).sum() / period
                down = -np.minimum(seed, 0).sum() / period
                rs = up / down
                rsi = np.zeros_like(prices)
                rsi[:period] = None  # Set first `period` values to None
            
                for i in range(period, len(prices)):
                    delta = deltas[i - 1]
                    if delta > 0:
                        upval = delta
                        downval = 0.
                    else:
                        upval = 0.
                        downval = -delta
            
                    up = (up * (period - 1) + upval) / period
                    down = (down * (period - 1) + downval) / period
                    rsi[i] = 100. - 100. / (1. + (up / down))
            
                return rsi
                    
            if topIndicator[0] == "rsi":
                rsi_values = calculateRSI(nifty["close"], topIndicator[1])
                a0.plot_date(data["datetime"], rsi_values, "#B59FDC", label = "RSI")
                mask_oversold = rsi_values < 30
                mask_overbought = rsi_values > 70
                a0.fill_between(data["datetime"],70, rsi_values, where = (mask_overbought), interpolate = True,alpha = 0.5, facecolor = "#FF8686", edgecolor = "#FF8686")
                a0.fill_between(data["datetime"], rsi_values, 30, where = (mask_oversold), interpolate = True,alpha = 0.5, facecolor = "#9CD39E", edgecolor = "#9CD39E")
                top_rsi_was_updated_and_hence_indicator_needs_update = False
                top_rsi_was_updated_and_hence_price_needs_update = False
            
            elif topIndicator == "macd":
                macd_line, signal_line, histogram = calculate_macd(nifty["close"])
                a0_limits = a0.get_ylim()
                
                if (a0_limits == (0, 100)):
                    a0.set_ylim()
                    
                a0.plot_date(data["datetime"], macd_line.values, "#2962FF")
                a0.plot_date(data["datetime"], signal_line.values, "#FF6D00")
                a0.fill_between(data["datetime"], histogram.values, 0, where = (histogram.values >= 0), interpolate = True,alpha = 0.5, facecolor = "#81C783", edgecolor = "#81C783")
                a0.fill_between(data["datetime"], histogram.values, 0, where = (histogram.values < 0), interpolate = True,alpha = 0.5, facecolor = "#FF6868", edgecolor = "#FF6868")
            if bottomIndicator[0] == "rsi":
                rsi_values = calculateRSI(nifty["close"], bottomIndicator[1])
                a3.plot_date(data["datetime"], rsi_values, "#B59FDC", label = "RSI")
                mask_oversold = rsi_values < 30
                mask_overbought = rsi_values > 70
                a3.fill_between(data["datetime"],70, rsi_values, where = (mask_overbought), interpolate = True,alpha = 0.5, facecolor = "#FF8686", edgecolor = "#FF8686")
                a3.fill_between(data["datetime"], rsi_values, 30, where = (mask_oversold), interpolate = True,alpha = 0.5, facecolor = "#9CD39E", edgecolor = "#9CD39E")
                bottom_rsi_was_updated_and_hence_indicator_needs_update = False
                bottom_rsi_was_updated_and_hence_price_needs_update = False
            elif bottomIndicator == "macd":
                macd_line, signal_line, histogram = calculate_macd(nifty["close"])
                a3_limits = a3.get_ylim()
                
                if (a3_limits == (0, 100)):
                    a3.set_ylim()
                a3.plot_date(data["datetime"], macd_line.values, "#2962FF")
                a3.plot_date(data["datetime"], signal_line.values, "#FF6D00")
                a3.fill_between(data["datetime"], histogram.values, 0, where = (histogram.values >= 0), interpolate = True,alpha = 0.5, facecolor = "#81C783", edgecolor = "#81C783")
                a3.fill_between(data["datetime"], histogram.values, 0, where = (histogram.values < 0), interpolate = True,alpha = 0.5, facecolor = "#FF6868", edgecolor = "#FF6868")
    
            if topIndicator != "none":
                plt.setp(a0.get_xticklabels(), visible = False)
            
            if bottomIndicator != "none":
                plt.setp(a2.get_xticklabels(), visible = False)
                a3.xaxis.set_major_locator(mticker.MaxNLocator(5))
                a3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))

            indicator_need_to_be_updated = False
            indicator_counter = 0


    
    
class stockCharter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,"OIP.ico")
        tk.Tk.wm_title(self, "Stock Charter")
        
        container = tk.Frame(master = self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(index=0, weight=1)
        container.grid_columnconfigure(index=0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = self.destroy)
        menubar.add_cascade(label="File", menu = filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff = 1)
        exchangeChoice.add_command(label ="BITSTAMP", command = lambda: changeExchange("BITSTAMP"))
        exchangeChoice.add_command(label ="COINBASE", command = lambda: changeExchange("COINBASE"))
        exchangeChoice.add_command(label ="BINANCE", command = lambda: changeExchange("BINANCE"))
        
        menubar.add_cascade(label="Exchange", menu = exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff = 1)
        dataTF.add_command(label = "1 minute", command = lambda: changeTimeframe("1min"))
        dataTF.add_command(label = "5 minute", command = lambda: changeTimeframe("5min"))
        dataTF.add_command(label = "15 minute", command = lambda: changeTimeframe("15min"))
        dataTF.add_command(label = "1 Hour", command = lambda: changeTimeframe("1h"))
        dataTF.add_command(label = "4 Hour", command = lambda: changeTimeframe("4h"))
        dataTF.add_command(label = "Daily", command = lambda: changeTimeframe("1d"))
        dataTF.add_command(label = "Weekly", command = lambda: changeTimeframe("1w"))
        dataTF.add_command(label = "Monthly", command = lambda: changeTimeframe("1mon"))
        
        
        menubar.add_cascade(label = "Data Time Frame", menu = dataTF)

        topIndicator = tk.Menu(menubar, tearoff = 1)
        topIndicator.add_command(label = "None", command = lambda: changeTopIndicator("none"))
        topIndicator.add_command(label = "RSI", command = lambda: changeTopIndicator("rsi"))
        topIndicator.add_command(label = "MACD", command = lambda: changeTopIndicator("macd"))
        menubar.add_cascade(label = "Top Indicator", menu = topIndicator)

        midIndicator = tk.Menu(menubar, tearoff = 1)
        midIndicator.add_command(label = "None", command = lambda: changeMidIndicator("none"))
        midIndicator.add_command(label = "SMA", command = lambda: changeMidIndicator("sma"))
        midIndicator.add_command(label = "EMA", command = lambda: changeMidIndicator("ema"))
        menubar.add_cascade(label = "Middle Indicator", menu = midIndicator)

        bottomIndicator = tk.Menu(menubar, tearoff = 1)
        bottomIndicator.add_command(label = "None", command = lambda: changeBottomIndicator("none"))
        bottomIndicator.add_command(label = "RSI", command = lambda: changeBottomIndicator("rsi"))
        bottomIndicator.add_command(label = "MACD", command = lambda: changeBottomIndicator("macd"))
        menubar.add_cascade(label = "Bottom Indicator", menu = bottomIndicator)

        tradeButton = tk.Menu(menubar, tearoff = 1)
        tradeButton.add_command(label = "Manual Trading", command = lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Automated Trading", command = lambda: popupmsg("This is not live yet"))
        tradeButton.add_separator()
        tradeButton.add_command(label = "Quick buy", command = lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Quick sell", command = lambda: popupmsg("This is not live yet"))
        tradeButton.add_separator()
        tradeButton.add_command(label = "Set up quick buy/sell", command = lambda: popupmsg("This is not live yet"))
        menubar.add_cascade(label = "Trading", menu = tradeButton)

        startStop = tk.Menu(menubar, tearoff = 1)
        startStop.add_command(label = "Resume", command = lambda: loadChart("start"))
        startStop.add_command(label = "Pause", command = lambda: loadChart("stop"))
        menubar.add_cascade(label = "Start/Stop", menu = startStop)

        helpMenu = tk.Menu(menubar, tearoff = 0)
        helpMenu.add_command(label = "Tutorial", command = tutorial)
        menubar.add_cascade(label = "Help", menu = helpMenu)

        #searchMenu = tk.Button(menubar, command=searchFunction)
        menubar.add_command(label = "Search", command=searchFunction)
         

        tk.Tk.config(self, menu = menubar)
        
        self.frames = {}

        for F in (startPage, pageOne, pageTwo, graphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.showFrame(startPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Live Cryptocurrency Charter",font=("Verdana",36))
        label1.place(x=570,y=100)

        label1 = tk.Label(self, text="Vyom Thakkar (A008)",font=("Verdana",26))
        label1.place(x=700,y=280)

        label1 = tk.Label(self, text="&",font=("Verdana",26))
        label1.place(x=920,y=380)

        label1 = tk.Label(self, text="Swara Keny (A010)",font=("Verdana",26))
        label1.place(x=730,y=480)
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.showFrame(pageOne))
        button2.place(x=1700,y=900)

class pageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Objectives",font=("Verdana", 36))
        label.pack(padx=10, pady=10)

        label1 = tk.Label(self, text='''• Stock Selection: Provide a dropdown menu or search functionality to allow users to select
their desired cryptocurrency (e.g., BTCUSD) for analysis.''',font=("Verdana", 20))
        
        label1.place(x=60,y=100)

        label1 = tk.Label(self, text='''• Providing different timeframes: Explore the distribution of cryptocurrency prices over different time intervals
(e.g., daily, weekly, monthly)''',font=("Verdana", 20))
        
        label1.place(x=60,y=250)

        label1 = tk.Label(self, text='''• Toolbar: Integrate a navigation toolbar with options for changing graph size.''',font=("Verdana", 20))
        
        label1.place(x=60,y=400)

        label1 = tk.Label(self, text='''• Techincal Indicators :Use of technical indicators analyze past price and volume data to help predict future 
market movements in trading and investing''',font=("Verdana", 20))
        
        label1.place(x=60,y=550)

        label1 = tk.Label(self, text='''• Graph Visualization: Utilize Matplotlib and FigureCanvasTkAgg to render interactive graphs and charts 
        within the application's GUI, and ensuring real-time updates and dynamic visualization.'''
,font=("Verdana", 20))
        
        label1.place(x=60,y=700)

        button1 = ttk.Button(self, text="Previous", command=lambda: controller.showFrame(startPage))
        button1.place(x=140,y=900)
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.showFrame(pageTwo))
        button2.place(x=1700,y=900)

class pageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select Cryptocurrency", font=largeFont)
        label.pack(padx=10, pady=10)

        selected_stock = tk.StringVar(self)
        selected_stock.set("--Select--")  
        stock_dropdown = tk.OptionMenu(self, selected_stock, *stock_list, command=lambda stock = selected_stock: changeStock(stock))
        stock_dropdown.pack()

        button1 = ttk.Button(self, text="Previous", command=lambda: controller.showFrame(pageOne))
        button1.place(x=140,y=900)
        
        button2 = ttk.Button(self, text="Next", command=lambda: controller.showFrame(graphPage))
        button2.place(x=1700,y=900)


class graphPage(tk.Frame):
    global stock_to_plot
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=bulletFont)
        label.pack(padx=5, pady=5)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.showFrame(startPage))
        button1.pack()
             
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = stockCharter()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=250)


app.mainloop()
