from fasthtml.common import *
import requests
user_objects = []    

app = FastHTML()

def pico_css_link():
    return Link("",rel="stylesheet",href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
def htmx_script_tag():
    return Script("",src="https://unpkg.com/htmx.org@2.0.2/dist/htmx.js",integrity="sha384-yZq+5izaUBKcRgFbxgkRYwpHhHHCpp5nseXp0MEQ1A4MTWVMnqkmcuFez8x5qfxr",crossorigin="anonymous")
def app_css_link():
    return Link("",rel="stylesheet",href="/app.css")

@app.get("/app.css")
def css():
    f=open("./app.css","r")
    return f.read()

@app.get("/")
def home():
    return Html(Head(Title("FastHTML101"),pico_css_link(),app_css_link()),init_body())

@app.get("/users")
def users():
    populate_users()
    return Div(search_input(),Table(users_table_thead(),users_table_tbody(user_objects)),id="users")

def init_body():
    return Body(Main(H1("Welcome!"),fetch_users_button(),loader(),Div("",id="users"),htmx_script_tag(),cls="container"))

def fetch_users_button():
    return Button("Fetch Users",hx_get="/users",hx_target="#users",hx_swap="outerHTML",hx_indicator="#loader")

def users_table_thead():
    return Thead(Tr(Th("Name"),Th("UserName"),Th("Email"),Th("Phone"),Th("Website")))

def users_table_tbody(users:list):
    return Tbody(*[users_table_row(user) for user in users])

def users_table_row(user:dict):
    return Tr(Td(user.name),Td(user.username),Td(user.email),Td(user.phone),Td(user.website))

def loader():
    return Div("",id="loader",aria_busy="true",cls="container")

def search_input():
    return Input("",type="text",name="search",placeholder="Search...")

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