from pipedrive.client import Client
import auth
import time

class Pipedrive: 

    def __init__(self) -> None:

        """
        Initalizes the users API token
        """
        
        self.authenticator = auth.Authentication()

        self.client = Client(domain='https://specifiedbuildingproducts-661b09.pipedrive.com/')
        self.client.set_api_token(self.authenticator.token)

    def get_state(self, address):
        parts = address.split(',')
        if len(parts) > 2:
            state_zip = parts[2].strip().split()
            if len(state_zip) > 0:
                self.state = state_zip[0]
        
    def get_company_details(self, participants):

        self.architect = ""
        self.lead_architect = ""
        self.general_contractor = ""
        self.lead_gc = ""

        for entry in participants:
            # print(entry)
            if entry['Company Role'] == 'Architect' or entry['Company Role'] == 'Awarded - Architect':
                self.architect = entry['Company Name']
                self.lead_architect = entry['Contact Name']
            elif entry['Company Role'] == 'General Contractor':
                self.general_contractor = entry['Company Name']
                self.lead_gc = entry['Contact Name']
    
    def create_new_deal(self, title, participants, address, id, task_text, notes):

        self.get_company_details(participants)
        self.get_state(address)

        self.org_id = 23569 #Placeholder - Construct Connect
        self.person_id = None

        self.check_org_and_lead()

        self.pipeline_id = 17
        self.stage_id = 114
        # gather data for deal

        data = {

            'title' : title,
            'org_id' : self.org_id,
            'person_id' : self.person_id,
            'pipeline_id' : self.person_id,
            'stage_id' : self.stage_id
        }

        # create the deal

        self.client.deals.create_deal(data)

        time.sleep(2)

        # get id of deal

        deal_id = self.get_deal_id(title)

        data = self.update_deal_fields(id)

        # update deal

        self.client.deals.update_deal(deal_id, data)

        self.post_note(notes, deal_id, self.org_id)
        self.post_task(task_text, deal_id, self.org_id)

    def check_org_and_lead(self):

        if self.architect != "":
            self.org_id = self.get_org_id(self.architect)
        elif self.general_contractor != "":
            self.org_id = self.get_org_id(self.general_contractor)
        
        if self.lead_architect != "":
            try:
                self.person_id = self.get_person_id(self.lead_architect)
            except:
                print("No person found in PD")
    
        elif self.general_contractor != "":
            try:
                self.person_id = self.get_person_id(self.lead_gc)
            except:
                print("No person found in PD")
    
    def get_person_id(self, name):

        params = {
            'term': name
        }

        person = self.client.persons.search_persons(params=params)
        person_data = person['data']
        if len(person_data["items"]) == 0:
            return None
        person_items = person_data['items'][0]
        person_item = person_items['item']
        person_id = person_item['id']
        return person_id
    
    def get_org_id(self, name):

        params = {
            'term': name
        }

        org = self.client.organizations.search_organizations(params=params)
        org_data = org['data']
        if len(org_data["items"]) == 0:
            return 23569
        org_items = org_data['items'][0]
        org_item = org_items['item']
        org_id = org_item['id']
        return org_id

    def update_deal_fields(self, id):

        data = {

            self.authenticator.business_unit : 'SBC',
            self.authenticator.deal_type : 'Commercial',
            self.authenticator.lead_source: 'Construct Connect',
            self.authenticator.business_rep: 'Todd Grant',
            self.authenticator.state: self.state,
            self.authenticator.architect: self.architect,
            self.authenticator.lead_architect: self.lead_architect,
            self.authenticator.general_contractor: self.general_contractor,
            self.authenticator.CC_id: id
        }
        
        return data

    def get_field_keys(self):

        """
        Method to get the keys for custom deal fields
        """

        response = self.client.deals.get_deal_fields()
        data = response["data"]
        
        return data

    def get_deal_id(self, deal_name):
        
        """
        Method to get the deal id from PD using the name of the deal
        """

        params = {
            'term': deal_name
        }

        deal = self.client.deals.search_deals(params=params)
        deal_data = deal['data']
        deal_items = deal_data['items'][0]
        deal_item = deal_items['item']
        deal_id = deal_item['id']
        return deal_id
    
    def post_task(self, task_text, deal_id, org_id):

        """ 
        Method to post the created task in PD 
        """
        
        data = {
            'subject':'Found in CC',
            'type':'task',
            'note':task_text,
            'deal_id':deal_id,
            'done':1,
            'org_id': org_id
        }

        reponse = self.client.activities.create_activity(data)
    
    def post_note(self, notes, deal_id, org_id):

        """
        Method to post the created note in PD
        """
        
        data = {
            'content':notes,
            'deal_id':deal_id,
            'pinned_to_deal_flag':1,
            'org_id': org_id
        }

        reponse = self.client.notes.create_note(data)