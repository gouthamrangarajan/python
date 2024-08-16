import requests
user_objects = []    

def check_user(user:dict,search:str):           
    if user.name.lower().find(search.lower())!=-1:
        return True
    elif user.username.lower().find(search.lower())!=-1:
        return True
    elif user.email.lower().find(search.lower())!=-1:
        return True
    elif user.website.lower().find(search.lower())!=-1:
        return True
    return False
    
def populate_users():
     # requests.packages.urllib3.disable_warnings()
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    if len(user_objects)>0:
        user_objects.clear()
    if response.status_code == 200: 
        users = response.json()
        for user_data in users:
            user = User(
                id=user_data['id'],
                name=user_data['name'],
                username=user_data['username'],
                email=user_data['email'],
                phone=user_data['phone'],
                website=user_data['website']
            )
            user_objects.append(user)

class User:
    def __init__(self,id, name, username, email, phone, website):
        self.id=id
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.website = website