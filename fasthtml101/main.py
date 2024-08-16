from fasthtml.common import *
from users_data import *

app = FastHTML()
user_table_sort=('name','asc')

def pico_css_link():
    return Link("",rel="stylesheet",href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
def pico_colors_link():
    return Link("",rel="stylesheet" ,href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css")
def htmx_script_tag():
    return Script("",src="https://unpkg.com/htmx.org@2.0.2",integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ",crossorigin="anonymous")
def app_css_link():
    return Link("",rel="stylesheet",href="/app.css")
def material_icons_link():
    return Link("",rel="stylesheet",href="https://fonts.googleapis.com/icon?family=Material+Icons")

@app.get("/app.css")
def css():
    f=open("./app.css","r")
    return f.read()

@app.get("/")
def home():
    return Html(Head(Title("FastHTML101"),Meta(name="viewport",content="width=device-width, initial-scale=1.0"),pico_css_link(),pico_colors_link(),material_icons_link(),app_css_link()),init_body())

@app.get("/users")
def users():
    populate_users()
    return Div(search_input(False),Div(Table(users_table_thead("",""),users_table_tbody(user_objects)),id="users_table",cls="overflow-auto"),id="users")

@app.post('/search')
def users_search(search:str):
    if len(user_objects)==0:
        populate_users()
    fted_users=[user for user in user_objects if check_user(user,search)]
    return Div(Table(users_table_thead("",""),users_table_tbody(fted_users)),id="users_table",cls="overflow-auto")

@app.post('/sort/{sort_key}/{direction}')
def sort(sort_key:str,direction:str):
    users=user_objects
    if(direction=='desc'):
        users=sorted(users,key=lambda x:x[sort_key],reverse=True)
    else:
        users=sorted(users,key=lambda x:x[sort_key])        
       
    return Div(Table(users_table_thead(sort_key,direction),users_table_tbody(users)),search_input(True),id="users_table",cls="overflow-auto")

def init_body():
    return Body(Main(H1("Welcome!"),fetch_users_button(),loader(),Div("",id="users"),htmx_script_tag(),cls="container"))

def fetch_users_button():
    return Button("Fetch Users",hx_get="/users",hx_target="#users",hx_swap="outerHTML",hx_indicator="#loader")

def users_table_thead(sort_key:str,sort_direction:str):   
    return Thead(Tr(users_table_thead_th("name","Name",sort_key,sort_direction),users_table_thead_th("username","UserName",sort_key,sort_direction),users_table_thead_th("email","Email",sort_key,sort_direction),users_table_thead_th("website","Website",sort_key,sort_direction)),id="users_thead")
    
def users_table_thead_th(key:str,heading:str,sort_key:str,sort_direction:str):
    if(sort_key==key):
        if(sort_direction=="asc"):
            return Th(heading,asc_sort_icon(),hx_post=f"/sort/{key}/desc",hx_trigger="click",hx_target="#users_table",hx_swap="outerHTML",hx_indicator="#loader")
        else:
            return Th(heading,desc_sort_icon(),hx_post=f"/sort/{key}/asc",hx_trigger="click",hx_target="#users_table",hx_swap="outerHTML",hx_indicator="#loader")
    return Th(heading,hx_post=f"/sort/{key}/asc",hx_trigger="click",hx_target="#users_table",hx_swap="outerHTML")

def users_table_tbody(users:list):
    return Tbody(*[users_table_row(user) for user in users],id="users_tbody")

def users_table_row(user:dict):
    return Tr(Td(user['name']),Td(user['username']),Td(user['email']),Td(user['website']),cls="animate-slide-down")

def loader():
    return Div("",id="loader",aria_busy="true",cls="container")

def search_input(isOob:bool):
    if isOob==False:
        return Input("",id="srchTxt",type="search",name="search",placeholder="Search...",hx_post="/search",hx_trigger="input changed delay:500ms, search",hx_target="#users_table",hx_indicator="#loader",hx_swap="outerHTML")
    else:
        return Input("",id="srchTxt",type="search",name="search",placeholder="Search...",hx_post="/search",hx_trigger="input changed delay:500ms, search",hx_target="#users_table",hx_indicator="#loader",hx_swap="outerHTML",hx_swap_oob="true")

def asc_sort_icon():
    return I("keyboard_arrow_up",cls="material-icons mt-2")

def desc_sort_icon():
    return I("keyboard_arrow_down",cls="material-icons mt-2")