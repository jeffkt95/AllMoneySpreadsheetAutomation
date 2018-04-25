from Account import Account

class SpreadsheetAccount(Account):

    def __init__(self, name, amount, column):
        Account.__init__(self, name, amount)
        self.column = column
        
    def getColumn(self):
        return self.column