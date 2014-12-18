import linkedin
from linkedin import linkedin # pip install python-linkedin
import json

# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application


RETURN_URL = '' # Not required for developer authentication
"https://www.linkedin.com/vsearch/p?type=people&keywords=seed%20funding&orig=FCTD&rsid=592041821416229890366&pageKey=voltron_people_search_internal_jsp&openFacets=N,G,CC&f_G=in%3A7151,in%3A7391,in%3A7392&page_num=2&pt=people"
# Pass it in to the app...
def chetan(
    CONSUMER_KEY    = '754qfrzwwbsvyl',
    CONSUMER_SECRET = 'rowEf1Kxfn5ZBtKX',
    USER_TOKEN      = '2d7c4ffe-96c2-4414-8708-fb28d290d550',
    USER_SECRET     = 'c14f1a47-30b6-4fca-b084-ab8a722b70eb'):
    auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
    return linkedin.LinkedInApplication(auth)
    
def rohit(
    CONSUMER_KEY    = '78z91mag242v9k',
    CONSUMER_SECRET = 'hleWJnYdqoDzTmG4',
    USER_TOKEN      = '40d2d0e3-5718-4f87-b31f-0693ab36c9f4',
    USER_SECRET     = '2492de07-88e5-4121-8cd9-8ec2674801ae'):
    auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
    return linkedin.LinkedInApplication(auth)
    
def sapna(
    CONSUMER_KEY    = '78k3j3e7r5nlqn',
    CONSUMER_SECRET = 'vnx9b1fFOuIqx7Hz',
    USER_TOKEN      = '3ca0c246-4562-495a-8291-272cc0eed95b',
    USER_SECRET     = '0382a409-308c-4957-9581-1a2a5c616f27'):
    auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
    return linkedin.LinkedInApplication(auth)

# Instantiate the developer authentication class
def api():
    return chetan() 

def profile(app, mem_id=None):
    return app.get_profile(member_id = mem_id)

def conn(app, mem_id=None):
    print mem_id
    return app.get_connections(member_id = mem_id)
#connections 

# Use the app...
def dump_conn(mem_id = None, name="chetan"):
    if name == "chetan":
        app = chetan()
    elif name == "rohit":
        app = rohit()
    else:
        app = sapna()
    connections_data = 'linkedin_conn-' + name +'.json'
    connections = conn(app, mem_id)
    if mem_id:
        connections_data = str(mem_id) + connections_data
    f = open(connections_data, 'w')
    f.write(json.dumps(connections, indent=1))
    f.close()
