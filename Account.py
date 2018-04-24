class Account:
    
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        
    def getName(self):
        return self.name
        
    def getAmount(self):
        return self.amount
        
    def __str__(self):
        #print("Trying to return string for account with name " + self.name)
        #print("   Trying to return string for account with amount " + self.amount)
        #print("Account " + self.name + ", amount " + str(self.amount))
        
        #accountString = "Account "
        #accountString += self.name
        #accountString += ", amount "
        #accountString += str(self.amount)
        
        accountString = "Account " + self.name + ", amount=" + str(self.amount)
        return accountString