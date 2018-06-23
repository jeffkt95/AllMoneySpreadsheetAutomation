import mintapi

class MintConnection:

    def __init__(self, username, password):
        self.mint = mintapi.Mint(username, password)
        print("Refreshing mint accounts...")
        #self.mint.initiate_account_refresh()
        self.mint.refresh_accounts()
        print("Accounts refreshed!")
        self.accounts = self.mint.get_accounts()
        mintapi.print_accounts(self.accounts)
        
    def getAccounts(self):
        return self.accounts
        