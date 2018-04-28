from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable
from MintAccountsNameMap import MintAccountNotFound
import Utilities

class AllMoneySpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1MqfeN82WwZrRYT0wVPOGZSycg1-9bxNiPCYfDbHfFJA'
    REAL_SPREADSHEET_ID = '1wdMoEie0DjtNiMMkr11sVis5lO99aiwJJaLPl-u8JUk'
    LAST_ROW_NAMED_RANGE = "lastDataRow"
    DOW_DATA_COLUMN = "M"

    SHEET_NAME = "Data"
    
    #From START_COLUMN_COPY to END_COLUMN_COPY are calc'd cells that should just be copied from previous row.
    START_COLUMN_COPY = 14
    END_COLUMN_COPY = 19
    
    def __init__(self):
        GoogleSheetInterface.__init__(self, self.REAL_SPREADSHEET_ID)
        
    def addNewRowForData(self):
        rowNumber = self.getRowOfNamedRange(self.LAST_ROW_NAMED_RANGE)
        rowAdded = self.addRow(self.SHEET_NAME, rowNumber)
        self.copyPasteRow(self.SHEET_NAME, rowAdded - 1, rowAdded)
        
        dateStr = Utilities.getDateStr()
        self.setCellValue("A" + str(rowAdded), dateStr, self.SHEET_NAME)

        #Clear all data between columns 2 through 13
        self.setCellsValue("B" + str(rowAdded) + ":M" + str(rowAdded), [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""]], self.SHEET_NAME)
        
        return rowAdded
        
    def setDow(self, rowForNewData, dowValue):
        self.setCellValue(self.DOW_DATA_COLUMN + str(rowForNewData), dowValue, self.SHEET_NAME)
    
    def setAccountsData(self, accountsFromMint, mintAccountsNameMap, rowToUpdate):
        for accountFromMint in accountsFromMint:
            try:
                spreadsheetAccount = mintAccountsNameMap.getSpreadsheetAccount(accountFromMint)
                self.setAccountAmount(rowToUpdate, spreadsheetAccount.getColumn(), accountFromMint.getAmount())
            
            except MintAccountNotFound as err:
                continue
                #Fail silently. There are some random, unused Mint accounts that aren't in the map, by design.
                #print(err.message)
                    
    def setAccountAmount(self, rowNum, accountColumn, amount):
        cellAddress = accountColumn + str(rowNum)
        self.setCellValue(cellAddress, amount, self.SHEET_NAME)
        
