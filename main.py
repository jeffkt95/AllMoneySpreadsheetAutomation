import Utilities
from Accounts import Accounts
from AllMoneySpreadsheet import AllMoneySpreadsheet
from MintAccountsNameMap import MintAccountsNameMap
from MintConnection import MintConnection
from Accounts import ImproperlyFormattedMintData
import StockData
import webbrowser
from builtins import input
#import getpass

#Besides running the allMoneyScript, this method runs all the stuff you would do manually before and after
def main():
    webbrowser.open("https://mint.intuit.com/overview.event")
    wait = input("Copy account data from mint.com then press enter.")
    allMoneySpreadsheet = allMoneyScript(True)
    wait = input("All done!")
    
#This script grabs what's on the clipboard from a mint.com copy and puts it into the AllMoney spreadseheet in the right place.
#It also grabs the dow.
def allMoneyScript(launchSpreadsheet = False):
    accountsCopiedFromMint = Utilities.getClipboard()
    #password = getpass.getpass(prompt="Enter Mint password: ")
    #mintConnection = MintConnection("jeffkt@alum.mit.edu", password)

    accountsFromMint = Accounts()
    #accountsFromMint.getAccountsFromMintAccounts(mintConnection.getAccounts())
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
    
