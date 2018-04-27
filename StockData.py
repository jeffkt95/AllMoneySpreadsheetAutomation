import requests
import json
import Utilities

#Should be valid and free for life.
API_KEY = '4OPH40C80UJ8D4ES'
QUERYURL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=" + API_KEY
#Full URL example: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=4OPH40C80UJ8D4ES&symbol=DJI

#TODO: If the market is open, it gives you the current, moving value. I think I'd rather have it give me the value as of last close
def getStockPrice(symbol):
    url = QUERYURL + "&symbol=" + symbol
    response = requests.get(url)
    responseJson = json.loads(response.text)
    timeSeries = responseJson['Time Series (Daily)']

    #Starting from today and going back a maximum of three weeks, find the most recent data.
    mostRecentData = None
    dateToCheck = None
    for i in range(0, 21):
        dateToCheck = Utilities.getDateStrNumDaysAgo(i)
        if dateToCheck in timeSeries:
            mostRecentData = timeSeries[dateToCheck]
            break
    
    if (mostRecentData is not None):
        closingPrice = mostRecentData['4. close']
        print("Found " + symbol + " data for date " + dateToCheck + ". Close price is " + closingPrice)
        return closingPrice
    else:
        print("Couldn't find most recent data!")
        return -1
        #TODO: Throw an error
