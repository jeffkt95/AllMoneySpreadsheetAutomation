from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable
from MintAccountsNameMap import MintAccountNotFound
import Utilities

class AllMoneySpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1MqfeN82WwZrRYT0wVPOGZSycg1-9bxNiPCYfDbHfFJA'
    REAL_SPREADSHEET_ID = '1wdMoEie0DjtNiMMkr11sVis5lO99aiwJJaLPl-u8JUk'
    LAST_ROW_NAMED_RANGE = "lastDataRow"

    SHEET_NAME = "Data"
    
    #From START_COLUMN_COPY to END_COLUMN_COPY are calc'd cells that should just be copied from previous row.
    START_COLUMN_COPY = 14
    END_COLUMN_COPY = 19
    
    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        
    def addNewRowForData(self):
        rowNumber = self.getRowOfNamedRange(self.LAST_ROW_NAMED_RANGE)
        rowAdded = self.addRow(self.SHEET_NAME, rowNumber)
        self.copyPasteRow(self.SHEET_NAME, rowAdded - 1, rowAdded)
        
        dateStr = Utilities.getDateStr()
        self.setCellValue("A" + str(rowAdded), dateStr, self.SHEET_NAME)

        #Clear all data
        #Remove data in columns 2 through 13
        #TODO: Do this as a batch so it doesn't take so long?
        self.setCellValue("B" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("C" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("D" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("E" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("F" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("G" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("H" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("I" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("J" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("K" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("L" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("M" + str(rowAdded), "", self.SHEET_NAME)
        
        return rowAdded
    
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
        
