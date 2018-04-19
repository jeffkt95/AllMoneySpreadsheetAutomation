import datetime
import win32clipboard

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

def print_data(values):
    if not values:
        print('No data found.')
    else:
        print('Envelope name, Amount, Amount spent, Amount left, %spent')
        for row in values:
            # Print columns A, B, C, D, E
            if (len(row) >= 5):
                print('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))
