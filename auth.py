import json
import bcrypt
import base64

class Authentication:

    def __init__(self) -> None:

        with open('credentials.json', 'r') as openfile:

            creds = json.load(openfile)
        
        self.email = creds["email"]
        self.password = creds["password"]
        self.token = creds["token"]
    
    def changes_creds(self, email, password, token):
        
        with open('credentials.json', 'r') as openfile:

            creds = json.load(openfile)
        
        salt = bcrypt.gensalt()

        if email != "":
            creds["email"] = email
        if password != "":
            creds["password"] = password
        if token != "":
            creds["token"] = token

        with open('credentials.json', 'w') as f: 
            json.dump(creds, f, indent=4) 