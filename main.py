import Utilities
from Accounts import Accounts
from AllMoneySpreadsheet import AllMoneySpreadsheet
from MintAccountsNameMap import MintAccountsNameMap
import StockData

def main():
    accountsCopiedFromMint = Utilities.getClipboard()
    #with open('testData3.txt', 'r') as myfile:
    #    accountsCopiedFromMint = myfile.read()
    
    #TODO: gracefully handle empty or improperly formatted clipboard
    
    accountsFromMint = Accounts()
    accountsFromMint.getAccountsFromMintCopy(accountsCopiedFromMint)
    
    print(accountsFromMint)
    
    allMoneySpreadsheet = AllMoneySpreadsheet()
    print("Connecting to spreadsheet...")
    allMoneySpreadsheet.connect()
    print("Preparing spreadsheet for new data...")
    rowNum = allMoneySpreadsheet.addNewRowForData()
    
    mintAccountsNameMap = MintAccountsNameMap(allMoneySpreadsheet)
    
    print("Putting mint data into spreadsheet...")
    allMoneySpreadsheet.setAccountsData(accountsFromMint, mintAccountsNameMap, rowNum)
    
    print("Getting the DOW...")
    dowValue = StockData.getStockPrice("DJI")
    allMoneySpreadsheet.setDow(rowNum, dowValue)
    
    print("Done.")
    
if __name__ == "__main__":
    main()
    
