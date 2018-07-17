import datetime
import win32clipboard
from datetime import timedelta

def reverseSign(value):
    #Remove commas. Comma delimiters screw up casting as float.
    strWithoutCommas = value.replace(",", "")
    if (is_number(strWithoutCommas)):
        return -1 * float(strWithoutCommas)
    else:
        return value

#This function takes a string and tries to make it a number. It removes
#comma delimiters if they're there. If it can't cast as a float, it just
#returns the argument back.
def getNumber(value):
    #Remove commas. Comma delimiters screw up casting as float.
    strWithoutCommas = value.replace(",", "")
    if (is_number(strWithoutCommas)):
        return float(strWithoutCommas)
    else:
        return value
        
def is_number(s):
    try:
        #If the argument is a string, you want to remove commas first.
        #Comma delimiters screw up casting as float.
        if (isinstance(s, str)):
            s = s.replace(",", "")
        float(s)
        return True
    except ValueError:
        return False
  
def getDateStr():
    now = datetime.datetime.now()
    return str(now.strftime("%m/%d/%Y %H:%M"))

def getDateStrNumDaysAgo(numDaysAgo = 0):
    dateToReturn = datetime.datetime.now()
    
    for i in range(0, numDaysAgo):
        dateToReturn = dateToReturn - timedelta(days=1)
    
    return str(dateToReturn.strftime("%Y-%m-%d"))

def isDate(possibleDate):
    try:
        datetime.datetime.strptime(possibleDate, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def getClipboard():
    win32clipboard.OpenClipboard()
    try:
        fromClipboard = win32clipboard.GetClipboardData()
    except:
        #You can raise the exception if there's a failure, but you must close
        #the clipboard or copy/paste will stop working
        win32clipboard.CloseClipboard
        raise
    else:
        win32clipboard.CloseClipboard
        return fromClipboard
    
def print_data2(values):
    for i in range(len(values)):
        rowString = " "
        for j in range(len(values[i])):
            rowString = rowString +  "   " + str(values[i][j])
        print(rowString)

def print_data1(values):
    for value in values:
        print("'" + str(value) + "'")
