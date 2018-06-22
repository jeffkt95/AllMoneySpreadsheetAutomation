import Utilities
from Accounts import Accounts
from AllMoneySpreadsheet import AllMoneySpreadsheet
from MintAccountsNameMap import MintAccountsNameMap
from Accounts import ImproperlyFormattedMintData
import StockData
import webbrowser
from builtins import input

import requests
import logging
import sys
import mintapi

# Enabling debugging at http.client level (requests->urllib3->http.client)
# you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# the only thing missing will be the response.body which is not logged.
try: # for Python 3
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection
HTTPConnection.debuglevel = 0

#Besides running the allMoneyScript, this method runs all the stuff you would do manually before and after
def main():
    tryMintApi()

    #webbrowser.open("https://mint.intuit.com/overview.event")
    #wait = input("Copy account data from mint.com then press enter.")
    #allMoneySpreadsheet = allMoneyScript(True)
    #wait = input("All done!")
    
def tryMintApi():
    mint = mintapi.Mint('jeffkt@alum.mit.edu', 'Jkjc9511!')
    accounts = mint.get_accounts()
    mint.initiate_account_refresh()
    print(accounts)
    
def tryMintLogin():
    #mintUrl = "https://mint.intuit.com/overview.event"
    mintUrl = "https://mint.intuit.com"
    overviewPage = mintUrl + "/overview.event"
    
    session = requests.Session()
    #session.config['verbose'] = sys.stderr
    
    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True    
    
    login_data = {
        'loginemail': 'jeffkt@alum.mit.edu',
        'loginpswd':  'Jkjc9511!',
        'submit': 'login',
    }
    
     # Authenticate
    response = session.post(mintUrl, data=login_data)
    #print(response.status_code)
    #print(response.text)

    # Try accessing a page that requires you to be logged in
    response = session.get(overviewPage)

    #response = requests.get(mintUrl, auth=('jeffkt@alum.mit.edu', 'Jkjc9511!'))
    #print(response.status_code)
    #print(response.text)

    
#This script grabs what's on the clipboard from a mint.com copy and puts it into the AllMoney spreadseheet in the right place.
#It also grabs the dow.
def allMoneyScript(launchSpreadsheet = False):
    accountsCopiedFromMint = Utilities.getClipboard()
    #with open('testData3.txt', 'r') as myfile:
    #    accountsCopiedFromMint = myfile.read()
    
    accountsFromMint = Accounts()
    try:
        accountsFromMint.getAccountsFromMintCopy(accountsCopiedFromMint)
    except ImproperlyFormattedMintData as err:
        print("Error: " + err.message)
        print("Quitting.")
        return
    
    print(accountsFromMint)
    
    allMoneySpreadsheet = AllMoneySpreadsheet()
    print("Connecting to spreadsheet...")
    allMoneySpreadsheet.connect()
    print("Preparing spreadsheet for new data...")
    rowNum = allMoneySpreadsheet.addNewRowForData()
    
    if (launchSpreadsheet):
        webbrowser.open(allMoneySpreadsheet.getSpreadsheetUrl())
    
    mintAccountsNameMap = MintAccountsNameMap(allMoneySpreadsheet)
    
    print("Putting mint data into spreadsheet...")
    allMoneySpreadsheet.setAccountsData(accountsFromMint, mintAccountsNameMap, rowNum)
    
    print("Getting the DOW and S&P500...")
    try:
        dowValue = StockData.getStockPrice("DJI")
        allMoneySpreadsheet.setDow(rowNum, dowValue)
        spValue = StockData.getStockPrice("SPX")
        allMoneySpreadsheet.setSpIndex(rowNum, spValue)
    except Exception as err:
        print("Error getting stock values: " + str(err))
    
    print("Done.")
    
    return allMoneySpreadsheet
    
if __name__ == "__main__":
    main()
    
