import json

class Authentication:

    def __init__(self) -> None:

        with open('credentials.json', 'r') as openfile:
 
            # Reading from json file
            creds = json.load(openfile)
        
        self.email = creds["email"]
        self.password = creds["password"]
        self.token = creds["token"]
    
    def changes_creds(self, email, password, token):
        pass