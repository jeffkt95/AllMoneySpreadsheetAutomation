from GoogleSheetInterface import GoogleSheetInterface
from MintAccountsNameMap import MintAccountNotFound
import Utilities

class AllMoneySpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1MqfeN82WwZrRYT0wVPOGZSycg1-9bxNiPCYfDbHfFJA'
    REAL_SPREADSHEET_ID = '1wdMoEie0DjtNiMMkr11sVis5lO99aiwJJaLPl-u8JUk'
    #Change this next variable based on whether you are testing or this is for real
    SPREADSHEET_TO_USE = REAL_SPREADSHEET_ID

    LAST_ROW_NAMED_RANGE = "lastDataRow"
    DOW_DATA_COLUMN = "N"
    SPINDEX_DATA_COLUMN = "O"

    SHEET_NAME = "Data"

    #From START_COLUMN_COPY to END_COLUMN_COPY are calc'd cells that should just be copied from previous row.
    START_COLUMN_COPY = 16
    END_COLUMN_COPY = 21

    mRowData = 0

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.SPREADSHEET_TO_USE)

    def getSpreadsheetUrl(self):
        spreadsheetId = self.getSpreadsheetId()
        return "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/edit#gid=0&range=A" + str(self.mRowData - 1)

    def addNewRowForData(self):
        self.mRowData = self.getRowOfNamedRange(self.LAST_ROW_NAMED_RANGE)
        self.mRowData = self.addRow(self.SHEET_NAME, self.mRowData)
        self.copyPasteRow(self.SHEET_NAME, self.mRowData - 1, self.mRowData)

        dateStr = Utilities.getDateStr()
        self.setCellValue("A" + str(self.mRowData), dateStr, self.SHEET_NAME)
        self.formatCell(self.mRowData, 1, "m/d/yyyy", self.SHEET_NAME)

        #Clear all data between columns 2 through 14
        self.setCellsValue("B" + str(self.mRowData) + ":N" + str(self.mRowData), [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""], [""]], self.SHEET_NAME)

        return self.mRowData

    def setDow(self, rowForNewData, dowValue):
        self.setCellValue(self.DOW_DATA_COLUMN + str(rowForNewData), dowValue, self.SHEET_NAME)

    def setSpIndex(self, rowForNewData, spValue):
        self.setCellValue(self.SPINDEX_DATA_COLUMN + str(rowForNewData), spValue, self.SHEET_NAME)

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
