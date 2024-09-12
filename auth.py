import json
import bcrypt
import base64
import os
import sys

class Authentication:

    def __init__(self) -> None:

        """
        Method to load credentials from json file at initalization.
        """

        self.json_path = self.resource_path('credentials_exe.json')

        with open(self.json_path, 'r') as openfile:

            creds = json.load(openfile)
        
        self.email = creds["email"]
        self.password = creds["password"]
        self.token = creds["token"]

        self.business_unit = creds['Business Unit']
        self.deal_type = creds['Deal Type']
        self.architect = creds['Architect']
        self.lead_architect = creds['Lead Architect']
        self.general_contractor = creds['General Contractor']
        self.lead_source = creds['Lead Source']
        self.CC_id = creds['ConstructConn Project ID#']
        self.business_rep = creds['Business Development Rep']
        self.state = creds['State']

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return os.path.join(os.path.abspath("."), 'credentials.json')
    
    def changes_creds(self, email, password, token, key_fields):

        """
        Method to change credentials using json.
        """
        
        with open(self.json_path, 'r') as openfile:

            creds = json.load(openfile)
        
        salt = bcrypt.gensalt()

        field_names = ['Business Unit', 'Deal Type', 'Architect', 'Lead Architect', 'General Contractor', 'Lead Source', 'ConstructConn Project ID#', 'Business Development Rep', 'State']

        if email != "":
            creds["email"] = email
        if password != "":
            creds["password"] = password
        if token != "":
            creds["token"] = token

        if key_fields:
            for entry in key_fields:
                if entry['name'] in field_names:
                    creds[entry['name']] = entry['key']

        with open(self.json_path, 'w') as f: 
            json.dump(creds, f, indent=4)

    def get_deal_field_keys(self, data):
        pass
