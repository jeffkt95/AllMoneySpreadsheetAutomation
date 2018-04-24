from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable
import Utilities

class AllMoneySpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1MqfeN82WwZrRYT0wVPOGZSycg1-9bxNiPCYfDbHfFJA'
    REAL_SPREADSHEET_ID = '1wdMoEie0DjtNiMMkr11sVis5lO99aiwJJaLPl-u8JUk'
    #SPENT_TOTAL_NAMED_RANGE = "SpentTotal"
    #ENVELOPE_DATE_NAMED_RANGE = "AllEnvelopeData"
    #AMOUNT_SPENT_NAMED_RANGE = "AmountSpent"
    LAST_ROW_NAMED_RANGE = "lastDataRow"

    SHEET_NAME = "Data"

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        #self.mEnvelopesTable = GoogleSheetsTable(self, "A", "B", 3, 32, self.SHEET_NAME)
        
    #def getEnvelopesTable(self):
    #    return self.mEnvelopesTable
        
    #def loadEnvelopeData(self):
    #    result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
    #                                                        range=self.ENVELOPE_DATE_NAMED_RANGE).execute()
    #    return result
    
    #def addToTotal(self, amountToAdd):
    #    totalCellAddress = "'" + self.SHEET_NAME + "'!" + self.TOTAL_CELL
    #    self.addToCell(totalCellAddress, amountToAdd)
    
    def addNewRowForData(self):
        #Skip first two empty rows; start in row 3
        rowNumber = self.getFirstEmptyRow(self.SHEET_NAME, 3)
        rowAdded = self.addRow(self.SHEET_NAME, rowNumber)
        self.copyPasteRow(self.SHEET_NAME, rowAdded - 1, rowAdded)
        
        #Clear all data
        #Remove data in columns 2 through 13, except for 5 and 11
        self.setCellValue("B" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("C" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("D" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("F" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("G" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("H" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("I" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("J" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("L" + str(rowAdded), "", self.SHEET_NAME)
        self.setCellValue("M" + str(rowAdded), "", self.SHEET_NAME)
        
        #TODO: set date cell (column A) to today's date
        
        return rowAdded
    
    def setAccountDataForRow(self, accounts, rowNum):
        for account in accounts:
            accountColumn = self.getAccountColumn(account.name)
            self.setAccountAmount(rowNum, accountColumn, account.amount)
        
    def getAccountColumn(self, accountName):
        #TODO: find account name
        return 1
        
    #This method takes in the envelopeData, finds the particular envelope, then sets the data
    def setAccountAmount(self, rowNum, accountColumn, amount):
        print("TODO setAccountAmount for [" + str(rowNum) + ", " + str(accountColumn) + "] = " + str(amount))
        #envelopeName = envelope.getName()
        #envelopeSpent = envelope.getAmountSpent()

        #for i in range(0, len(envelopeData)):
        #    if (envelopeData[i][0] == envelopeName):
        #        amountSpent[i] = [envelopeSpent]
                #print("Envelope " + envelopeName + " amount spent changed to " + str(envelopeSpent))
        #        return amountSpent
                
        #If you get down here without returning, you never found the envelope. Return envelopeData unmodified
        #print("Never found envelope " + envelopeName + "! " + str(envelopeSpent) + " won't be included.")
        #return amountSpent
        
