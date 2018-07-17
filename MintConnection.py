import mintapi
import random

class MintConnection:

    def __init__(self, username, password):
        self.mint = mintapi.Mint(username, password)
        #print("Refreshing mint accounts...")
        #self.mint.initiate_account_refresh()
        #self.refresh_accounts()
        #print("Accounts refreshed!")
        self.accounts = self.mint.get_accounts()
        mintapi.print_accounts(self.accounts)
        
    def getAccounts(self):
        return self.accounts
        
    #This method was in the mintapi, but they removed it.
    def refresh_accounts(self, max_wait_time=60, refresh_every=10):
        """Initiate an account refresh and wait for the refresh to finish.
        Returns number of accounts in error, or -1 if timed out."""
        print("Initiating a refresh")
        self.mint.initiate_account_refresh()
        waited = 0
        while True:
            print("About to 'request_and_check'. I've waited " + str(waited))
            json_headers = {'accept': 'application/json'}
            result = self.mint.request_and_check(
                'https://wwws.mint.com/userStatus.xevent?rnd=' +
                str(random.randint(0, 10**14)),
                headers=json_headers,
                expected_content_type='application/json')
            print("Got it!")
            data = json.loads(result.text)
            if data['isRefreshing'] is False:
                return data['errorCount']
            elif waited > max_wait_time/refresh_every:
                return -1
            else:
                waited += 1
                time.sleep(refresh_every)
