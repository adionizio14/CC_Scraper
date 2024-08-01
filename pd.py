from pipedrive.client import Client
import auth

authenticator = auth.Authentication()

client = Client(domain='https://specifiedbuildingproducts-661b09.pipedrive.com/')
client.set_api_token(authenticator.token)

