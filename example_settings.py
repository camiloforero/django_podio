#encoding:utf-8
from __future__ import unicode_literals
#This url is used by the hook generator to tell PODIO where the callback URL should be relative to the root domain
HOOK_URL = "podio/hooks" #No slashes at the beginning or in the end
#The domain where the hooks should arrive
DOMAIN = "http://ec2-52-24-60-163.us-west-2.compute.amazonaws.com" #No slash, please specify the protocol
#The client ID and client secret key to be used for interacting with PODIO. More information can be found in https://developers.podio.com/api-key
CLIENT_ID = "put_your_client_id_here"
CLIENT_SECRET = "put_your_client_secret_key_here"
#Login information for an user with appropriate permissions in case user login is needed
USER = "user@example.com"
PASSWORD = "password"
