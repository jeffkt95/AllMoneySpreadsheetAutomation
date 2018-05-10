from Account import Account

class Accounts:

    def __init__(self):
        self.accounts = []

        #Used for iteration
        self.accountIndex = 0
    
    def addAccount(self, name, amount):
        newAccount = Account(name, amount)
        self.accounts.append(newAccount)
        
    #Very simple check that the data is roughly what we expect
    def properlyFormattedData(self, mintData):
        if ("ACCOUNTS" in mintData and "WORTH" in mintData):
            return True
        else:
            return False
        
    def getAccountsFromMintCopy(self, allMoneyData):
        if (self.properlyFormattedData(allMoneyData) == False):
            raise ImproperlyFormattedMintData("Copied data appears improperly formatted. Did you copy the data from mint.com?")
        
        lines = allMoneyData.split("\n")
        
        for line in lines:
            #Remove the carriage return. It screws things up.
            line = line.replace("\r", "")

            periodIndex = line.find(".")
            if (periodIndex != -1 and periodIndex + 3 < len(line)):
                amount = line[:periodIndex+3]
                #Remove the $ and , from the amount string
                amount = amount.replace("$", "")
                amount = amount.replace(",", "")
                accountName = line[periodIndex+3:]
                self.addAccount(accountName, amount)
        
    def __str__(self):
        string = "Accounts:\n"
        totalAmount = 0
        for account in self.accounts:
            string = string + "    " + str(account) + "\n"
            totalAmount = totalAmount + float(account.getAmount())
        
        string = string + "TOTAL AMOUNT: " + str(totalAmount)
        return string
        
    def __iter__(self):
        return self
        
    #Required for Python 3
    def __next__(self):
        if (self.accountIndex >= len(self.accounts)):
            raise StopIteration
        else:
            self.accountIndex += 1
            return self.accounts[self.accountIndex - 1]
    
    #Required for python 2
    def next(self):
        return self.__next__()
        
class ImproperlyFormattedMintData(Exception):
    def __init__(self, message):
        self.message = message
            