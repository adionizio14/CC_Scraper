from pipedrive.client import Client
import auth

class Pipedrive: 

    def __init__(self) -> None:
        
        authenticator = auth.Authentication()

        self.client = Client(domain='https://specifiedbuildingproducts-661b09.pipedrive.com/')
        self.client.set_api_token(authenticator.token)

    def get_deal_id(self, deal_name):

        params = {
            'term': deal_name
        }

        deal = self.client.deals.search_deals(params=params)
        deal_data = deal['data']
        deal_items = deal_data['items'][0]
        deal_item = deal_items['item']
        deal_id = deal_item['id']
        return deal_id
    
    def post_task(self, task_text, deal_id):
        
        data = {
            'subject':'Found in CC',
            'type':'task',
            'note':task_text,
            'deal_id':deal_id,
            'done':1
        }

        reponse = self.client.activities.create_activity(data)
    
    def post_note(self, notes, deal_id):
        
        data = {
            'content':notes,
            'deal_id':deal_id,
            'pinned_to_deal_flag':1
        }

        reponse = self.client.notes.create_note(data)

# test = Pipedrive()

# task_text = (
#     f"Estimate Value:  <b>hi</b><br>"
#     f"Stage:  <b>hi</b><br>"
#     f"Category:  <b>hi</b><br>"
#     f"Address:  <b>hi</b><br>"
#     f"Listed on CC:  <b>hi</b><br>"
#     f"Start Date:  <b>hi</b>"
# )
# test.post_task(task_text, 20517)
