import requests
user_objects = []    

def check_user(user:dict,search:str):           
    if user['name'].lower().find(search.lower())!=-1:
        return True
    elif user['username'].lower().find(search.lower())!=-1:
        return True
    elif user['email'].lower().find(search.lower())!=-1:
        return True
    elif user['website'].lower().find(search.lower())!=-1:
        return True
    return False
    
def populate_users():
     # requests.packages.urllib3.disable_warnings()
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    if len(user_objects)>0:
        user_objects.clear()
    if response.status_code == 200: 
        users = response.json()
        for user in users:            
            user_objects.append(user)

        
    