#Title: Stock Price Checker Program
#Author: Brandon Hocking
#Description: Checks the current price of a stock after retrieving input from user in the form of the stock ticker symbol.
#Allows for plotting of the price of the stock over a span of one day, one week, one month, or one year.
#Version: 1.0


import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QInputDialog, QVBoxLayout, QLabel)
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


stk = ""
ticker = ""

class StockCheck(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Go To Stock Input', self)
        self.btn.clicked.connect(self.inputStock)

        self.instruct = QLabel(self)
        self.instruct.setText("Please Input A Stock Ticker.")

        self.stockName = QLabel(self)
        self.stockName.setText("Stock Name: ")

        self.l = QLabel(self)
        self.l.setText("Current Price: ")

        self.timespan = QLabel(self)
        self.timespan.setText("Timespan: ")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.plotbtn = QPushButton('Plot Options', self)
        self.plotbtn.clicked.connect(self.plotMenu)

        layout = QVBoxLayout()
        layout.addWidget(self.instruct)
        layout.addWidget(self.canvas)
        layout.addWidget(self.stockName)
        layout.addWidget(self.l)
        layout.addWidget(self.timespan)
        layout.addWidget(self.btn)
        layout.addWidget(self.plotbtn)
        self.setLayout(layout)

        self.canvas.hide()
        self.stockName.hide()
        self.l.hide()
        self.timespan.hide()
        self.plotbtn.hide()

        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Stock Price Checker')
        self.show()

    # Opens Input Dialog for User. If User enters stock ticker, Widgets and Plot are shown.
    def inputStock(self):
        global ticker, stk
        ok = False
        ticker = ""
        while ticker == "":                                                                                              #If user enters nothing, this reopens input window.
            ticker, ok = QInputDialog.getText(self, 'Stock Price Retriever', 'Input the Ticker for your Stock: ')
        stk = yf.Ticker(ticker)
        stock_price = self.getStockPrice(ticker)
        if ok:                                                                                                          #Shows previously hidden widgets, sets stock information
            self.l.setText(stock_price)
            self.stockName.setText("Stock Name: " + ticker)
            self.plotDayOpen()
            self.canvas.show()
            self.plotbtn.show()
            self.stockName.show()
            self.l.show()
            self.timespan.show()
            self.instruct.hide()
            self.setGeometry(300, 300, 700, 600)

#Retrieves the stock price using yfinance and inserts into string for the Main Window
    def getStockPrice(self, text):
        stk = yf.Ticker(text)
        info = stk.info
        stockPrice = "Current Price: $" + str(info.get("regularMarketPrice"))
        return stockPrice

#Plots one year of stock opening price, by day.
    def plotYearOpen(self):
        global ticker, stk
        hist = stk.history(period="1y")
        openPrice = (hist["Open"])
        priceArray = []
        for x in openPrice:
            priceArray.append(x)
        labelArray = openPrice.keys()
        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.plot(labelArray, priceArray)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(12))
        for tick in ax1.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("right")
        plt.title("One Year Plot of Price (" + ticker + ")" )
        self.plotOptions()
        self.timespan.setText("Timespan: One year")

#Plots one month of stock opening price, by interval of one hour.
    def plotMonthOpen(self):
        global ticker, stk
        hist = stk.history(period="1mo", interval="1h")
        openPrice = (hist["Open"])
        priceArray = []
        for x in openPrice:
            priceArray.append(x)
        labelArray = openPrice.keys()
        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.plot(labelArray, priceArray)
        plt.title("One Month Plot of Price (" + ticker + ")")
        ax1.xaxis.set_major_locator(plt.MaxNLocator(15))
        for tick in ax1.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("right")
        self.plotOptions()
        self.timespan.setText("Timespan: One Month")

#Plots one week of opening prices, by intervals of 30 minutes.
    def plotWeekOpen(self):
        global ticker, stk
        hist = stk.history(period="5d", interval="30m")
        openPrice = (hist["Open"])
        priceArray = []
        for x in openPrice:
            priceArray.append(x)
        labelArray = openPrice.keys()
        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.plot(labelArray, priceArray)
        for tick in ax1.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("right")
        plt.title("One Week Plot of Price (" + ticker + ")")
        self.plotOptions()
        self.timespan.setText("Timespan: One Week")

#Plots one day of opening prices, by intervals of 2 minutes.
    def plotDayOpen(self):
        global ticker, stk
        hist = stk.history(period="1d", interval="2m")
        openPrice = (hist["Open"])
        priceArray = []
        for x in openPrice:
            priceArray.append(x)
        labelArray = openPrice.keys()
        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        type(labelArray)
        x = 0
        time = []
        for dt in labelArray.astype(object):
            if dt.minute < 10:
                time.append(str(str(dt.hour) + ":0" + str(dt.minute)))
            else:
                time.append(str(str(dt.hour) + ":" + str(dt.minute)))
        ax1.plot(time, priceArray)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(15))
        plt.title("One Day Plot of Price (" + ticker + ")")

        self.plotOptions()
        self.timespan.setText("Timespan: One Day (Default)")

#Sets standard options for all four plots.
    def plotOptions(self):
        plt.xlabel("Date")
        plt.ylabel("Stock Price ($)")
        plt.xticks(rotation = 45)
        plt.gcf().subplots_adjust(bottom=0.25)
        self.canvas.draw()

#Brings up the Input Menu to select a plotting option.
    def plotMenu(self):
        plot, ok = QInputDialog.getItem(self, 'Plot Menu', 'Timespan of Plot', ['One Day', 'One Week (5 Days)','One Month (30 Days)',
                                                                                   'One Year (365 Days)'])
        if plot == 'One Day':
            self.plotDayOpen()
        elif plot == 'One Week (5 Days)':
            self.plotWeekOpen()
        elif plot == 'One Month (30 Days)':
            self.plotMonthOpen()
        elif plot == 'One Year (365 Days)':
            self.plotYearOpen()



#Runs the program.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StockCheck()
    sys.exit(app.exec_())
