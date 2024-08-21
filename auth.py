import json
import bcrypt
import base64

class Authentication:

    def __init__(self) -> None:

        """
        Method to load credentials from json file at initalization.
        """

        with open('credentials.json', 'r') as openfile:

            creds = json.load(openfile)
        
        self.email = creds["email"]
        self.password = creds["password"]
        self.token = creds["token"]
    
    def changes_creds(self, email, password, token, key_fields):

        """
        Method to change credentials using json.
        """
        
        with open('credentials.json', 'r') as openfile:

            creds = json.load(openfile)
        
        salt = bcrypt.gensalt()

        field_names = ['Business Unit', 'Deal Type', 'Architect', 'Lead Architect', 'General Contractor', 'Lead Source', 'ConstructConn Project ID#', 'Business Development Rep', 'State']

        if email != "":
            creds["email"] = email
        if password != "":
            creds["password"] = password
        if token != "":
            creds["token"] = token

        for entry in key_fields:
            if entry['name'] in field_names:
                creds[entry['name']] = entry['key']

        with open('credentials.json', 'w') as f: 
            json.dump(creds, f, indent=4)

    def get_deal_field_keys(self, data):
        pass
