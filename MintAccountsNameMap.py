from SpreadsheetAccount import SpreadsheetAccount

class MintAccountsNameMap():

    SHEET_NAME = "MintAccountsNameMap"
    TABLE_NAME = "mintAccountsNameMapTable"
    
    def __init__(self, parentSpreadsheet):
        self.mParentSpreadsheet = parentSpreadsheet
        
        resultSet = self.mParentSpreadsheet.getResultsSet(self.TABLE_NAME)
        self.mTable = resultSet.get('values', [])
        
    def printIt(self):
        print(type(self.mTable))
        print(self.mTable)
        
    def getSpreadsheetAccount(self, mintAccount):
        for i in range(0, len(self.mTable)):
            row = self.mTable[i]
            if (len(row) > 1):
                tableMintName = row[0]
                
                if (mintAccount.getName() == tableMintName):
                    tableSpreadsheetName = row[1]
                    tableSpreadsheetColumn = row[2]
                    spreadsheetAccount = SpreadsheetAccount(tableMintName, mintAccount.getAmount(), tableSpreadsheetColumn)
                    return spreadsheetAccount
        
        raise MintAccountNotFound("Mint account '" + mintAccount.getName() + "' not found in map") 
                
class MintAccountNotFound(Exception):
    def __init__(self, message):
        self.message = message
