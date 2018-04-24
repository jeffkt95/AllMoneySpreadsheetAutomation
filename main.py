import Utilities
from Accounts import Accounts
from AllMoneySpreadsheet import AllMoneySpreadsheet

def main():
    #allMoneyData = Utilities.getClipboard()
    with open('testData.txt', 'r') as myfile:
        allMoneyData = myfile.read()
    #TODO: gracefully handle empty or improperly formatted clipbard
    
    accounts = Accounts()
    accounts.getAccountsFromMintCopy(allMoneyData)
    
    print(accounts)
    
    allMoneySpreadsheet = AllMoneySpreadsheet()
    allMoneySpreadsheet.connect()
    rowNum = allMoneySpreadsheet.addNewRowForData()
    print("Added row " + str(rowNum))
    #allMoneySpreadsheet.setAccountDataForRow(accounts, rowNum)
    
    
if __name__ == "__main__":
    main()
    
