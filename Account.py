class Account:
    
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        
    def getName(self):
        return self.name
        
    def getAmount(self):
        return self.amount
        
    def __str__(self):
        accountString = "Account " + self.name + ", amount=" + str(self.amount)
        return accountString