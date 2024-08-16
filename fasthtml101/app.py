from fasthtml.common import *
from users_data import *

app = FastHTML()

def pico_css_link():
    return Link("",rel="stylesheet",href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
def pico_colors_link():
    return Link("",rel="stylesheet" ,href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css")
def htmx_script_tag():
    return Script("",src="https://unpkg.com/htmx.org@2.0.2",integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ",crossorigin="anonymous")
def app_css_link():
    return Link("",rel="stylesheet",href="/app.css")

@app.get("/app.css")
def css():
    f=open("./app.css","r")
    return f.read()

@app.get("/")
def home():
    return Html(Head(Title("FastHTML101"),pico_css_link(),pico_colors_link(),app_css_link()),init_body())

@app.get("/users")
def users():
    populate_users()
    return Div(search_input(),Table(users_table_thead(),users_table_tbody(user_objects)),id="users",cls="overflow-auto")

@app.post('/search')
def users_search(search:str):
    if len(user_objects)==0:
        populate_users()
    fted_users=[user for user in user_objects if check_user(user,search)]
    return users_table_tbody(fted_users)

def init_body():
    return Body(Main(H1("Welcome!"),fetch_users_button(),loader(),Div("",id="users"),htmx_script_tag(),cls="container"))

def fetch_users_button():
    return Button("Fetch Users",hx_get="/users",hx_target="#users",hx_swap="outerHTML",hx_indicator="#loader")

def users_table_thead():
    return Thead(Tr(Th("Name"),Th("UserName"),Th("Email"),Th("Website")))

def users_table_tbody(users:list):
    return Tbody(*[users_table_row(user) for user in users],id="users_tbody")

def users_table_row(user:dict):
    return Tr(Td(user.name),Td(user.username),Td(user.email),Td(user.website),cls="animate-slide-down")

def loader():
    return Div("",id="loader",aria_busy="true",cls="container")

def search_input():
    return Input("",type="search",name="search",placeholder="Search...",hx_post="/search",hx_trigger="input changed delay:500ms, search",hx_target="#users_tbody",hx_indicator="#loader",hx_swap="outerHTML")