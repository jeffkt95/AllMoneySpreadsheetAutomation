import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import webbrowser
import Utilities

class GoogleSheetInterface:
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'
    SPREADSHEET_URL_ROOT = 'https://docs.google.com/spreadsheets/d/'

    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        
    def connect(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        
    def getResultsSet(self, queryRange):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                            range=queryRange).execute()
        return result
            
    #Gets the value of a single cell
    #If sheetName is None, the assumption is it's already embedded in the cell address. If not, then the code will concatentate
    #sheetName and cellAddress to get the full cell address.
    def getCellValue(self, cellAddress, sheetName = None):
        if (sheetName is not None):
            cellAddress = sheetName + "!" + cellAddress
            
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=cellAddress).execute()
        values = result.get('values', [])
        if (len(values) < 1):
            return None
        else:
            return values[0][0]

    def getCellAddress(self, sheetName, column, row):
        address = "'" + sheetName + "'!"
        address = address + column + str(row)
        return address

    #Gets the value of a single cell with a named range
    def getCellValueNamedRange(self, namedRange):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=namedRange).execute()
        values = result.get('values', [])
        return values[0][0]

    #Open up this spreadsheet in a web browser.
    def openSpreadsheet(self):
        spreadsheetUrl = self.SPREADSHEET_URL_ROOT + self.spreadsheetId
        webbrowser.open(spreadsheetUrl)
        
    #Sets the value of a single cell
    #If sheetName is None, the assumption is it's already embedded in the cell address. If not, then the code will concatenate
    #sheetName and cellAddress to get the full cell address.
    def setCellValue(self, cellAddress, value, sheetName = None):
        if (sheetName is not None):
            cellAddress = sheetName + "!" + cellAddress

        myBody = {u'range': cellAddress, u'values': [[str(value)]], u'majorDimension': u'ROWS'}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=cellAddress, body=myBody, valueInputOption='USER_ENTERED').execute()
    
    #Returns index to added row
    def addRow(self, worksheetName, aboveRow):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'insertDimension': {
                u'range': {
                    u'sheetId': str(worksheetId),
                    u'dimension': u'ROWS',
                    u'startIndex': str(aboveRow-1),
                    u'endIndex': str(aboveRow)
                }
            }
        }
        ]}
        
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()

        return aboveRow
        
    def copyPasteColumn(self, worksheetName, sourceColumn, destinationColumn):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'copyPaste': {
                u'source': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(0),
                    u'startColumnIndex': str(sourceColumn),
                    u'endColumnIndex': str(sourceColumn + 1)
                },
                u'destination': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(0),       #Leave out endRowIndex to include all rows
                    u'startColumnIndex': str(destinationColumn),
                    u'endColumnIndex': str(destinationColumn + 1)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()
    
    #Argument rows are 1-based
    def copyPasteRow(self, worksheetName, sourceRow, destinationRow):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'copyPaste': {
                u'source': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(sourceRow-1),     #Convert 1-based rows to 0-based indices
                    u'endRowIndex': str(sourceRow),
                    u'startColumnIndex': str(0),
                },
                u'destination': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(destinationRow-1),
                    u'endRowIndex': str(destinationRow),       
                    u'startColumnIndex': str(0)  #Leave out endColumnIndex to include all columns
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()

    #Argument rows are 1-based
    def copyPastePartOfRow(self, worksheetName, sourceRow, destinationRow, startColumnIndex, endColumnIndex):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'copyPaste': {
                u'source': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(sourceRow-1),     #Convert 1-based rows to 0-based indices
                    u'endRowIndex': str(sourceRow),
                    u'startColumnIndex': str(startColumnIndex),
                    u'endColumnIndex': str(endColumnIndex)
                },
                u'destination': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(destinationRow-1),
                    u'endRowIndex': str(destinationRow),       
                    u'startColumnIndex': str(startColumnIndex),
                    u'endColumnIndex': str(endColumnIndex)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()

    def insertColumn(self, columnIndex, worksheetName):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'insertDimension': {
                u'range': {
                    u'sheetId': str(worksheetId),
                    u'dimension': u'COLUMNS',
                    u'startIndex': str(columnIndex),
                    u'endIndex': str(columnIndex + 1)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()
        
    def deleteColumn(self, columnIndex, worksheetName):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'deleteDimension': {
                u'range': {
                    u'sheetId': str(worksheetId),
                    u'dimension': u'COLUMNS',
                    u'startIndex': str(columnIndex),
                    u'endIndex': str(columnIndex + 1)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()
        
    def addToCell(self, cellAddress, amountToAdd):
        originalPotValue = self.getCellValue(cellAddress)
        
        if (originalPotValue == None):
            originalPotValue = 0
        
        if (Utilities.is_number(originalPotValue) == False):
            originalPotValue = Utilities.getNumber(originalPotValue)
        else:
            originalPotValue = float(originalPotValue)
        
        if (Utilities.is_number(amountToAdd) == False):
            amountToAdd = Utilities.getNumber(amountToAdd)
        else:
            amountToAdd = float(amountToAdd)
                    
        #Set the value to the retrieved value plus the amountToAdd
        newPotValue = originalPotValue + amountToAdd
        self.setCellValue(cellAddress, str(newPotValue))
    
    def getWorksheetIdByName(self, worksheetName):
        # https://developers.google.com/sheets/samples/sheet#determine_sheet_id_and_other_properties
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId, fields='sheets.properties').execute()
        
        sheets = result.get('sheets', [])

        for sheetProperties in sheets:
            theProperties = sheetProperties.get('properties')
            title = theProperties.get('title')
            if title == worksheetName:
                return theProperties.get('sheetId')

        raise SheetNotFoundError(worksheetName, "getWorksheetIdByName, sheet '" + worksheetName + "' not found.")
    
    def getRowOfNamedRange(self, namedRange):
        namedRangeResponse = self.getResultsSet(namedRange)
        
        address = namedRangeResponse['range']
        #Get the chars between the ! and the :
        exclamationIndex = address.find("!")
        colonIndex = address.find(":")
        firstCell = address[exclamationIndex+1:colonIndex]
        
        #Check the first three characters to see if they are letters (the column)
        startIndex = 0
        for i in range(0,2):
            charToCheck = firstCell[i:i+1]
            if (Utilities.is_number(charToCheck) == False):
                startIndex = i+1
            else:
                break
                
        row = firstCell[startIndex:]
        return int(row)
    
    def getFirstEmptyRow(self, worksheetName, startRow = 1):
        #Use 0-based index. Change based to 1-based row index on return
        rowIndex = 0
        startIndex = startRow - 1
        
        resultsSet = self.getResultsSet(worksheetName + "!A:A")
        values = resultsSet.get('values', [])

        for i in range(0, len(values)):
            cellValue = values[i]
            
            if (i >= startIndex):
                if (len(cellValue) == 0):
                    return i + 1

        print("TODO: throw an error")
    
    def getNumRowsInWorksheet(self, worksheetName):
        # https://developers.google.com/sheets/samples/sheet#determine_sheet_id_and_other_properties
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId, fields='sheets.properties').execute()
        
        sheets = result.get('sheets', [])

        for sheetProperties in sheets:
            theProperties = sheetProperties.get('properties')
            title = theProperties.get('title')
            if title == worksheetName:
                gridProperties = theProperties.get('gridProperties')
                rowCount = gridProperties.get('rowCount')
                return rowCount

        raise SheetNotFoundError(worksheetName, "getNumRowsInWorksheet, sheet '" + worksheetName + "' not found.")
    
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        flags = None
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            #if flags:
            credentials = tools.run_flow(flow, store, flags)
            #else: # Needed only for compatibility with Python 2.6
            #    credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
        
class SheetNotFoundError(Exception):
    """Exception raised when a sheet is not found.

    Attributes:
        sheetName -- Name of sheet not found
        message -- explanation of the error
    """

    def __init__(self, sheetName, message):
        self.sheetName = sheetName
        self.message = message