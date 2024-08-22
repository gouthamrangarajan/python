from fasthtml.common import *

app=FastHTML()
db = database('todos.db')
if 'Todo' not in db.t: db.t['Todo'].create(id=int, item=str, done=bool, pk='id')
Todo = db.t['Todo'].dataclass()
todos=db.t['Todo']

def pico_css_link():
    return Link("",rel="stylesheet",href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
def pico_colors_link():
    return Link("",rel="stylesheet" ,href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css")
def htmx_script_tag():
    return Script("",src="https://unpkg.com/htmx.org@2.0.2",integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ",crossorigin="anonymous")
def app_css_link():
    return Link("",rel="stylesheet",href="/app.css")
def material_icons_link():
    return Link("",rel="preload",href="https://fonts.googleapis.com/icon?family=Material+Icons",onload="this.rel='stylesheet'",_as="style")

@app.get("/app.css")
def css():
    f=open("./app.css","r")
    data= f.read()
    f.close()
    return data

@app.get("/")
def home():
    return Html(Head(Title("FastHTML-ToDo"),Meta(name="color-schema",content="light dark"),Meta(name="viewport",content="width=device-width, initial-scale=1.0"),pico_css_link(),pico_colors_link(),material_icons_link(),app_css_link()),body())

@app.post("/")
def add_item(item:str):
    nextId=1
    if len(todos()) != 0:
        nextId=max([todo.id for todo in todos()])+1    
    todo=Todo(nextId,item,False)
    todos.insert(todo)
    return Tr(Td(Label(done_checkbox(nextId,False),item,delete_button(nextId)),scope="row"),cls="animate-slide-down",id=f'tr_{nextId}')

@app.post("/done/{itemId}")
def toggle_done(itemId:int):    
    item=next(filter(lambda item:item.id==itemId, todos()))  
    item.done=not item.done
    todos.update(item)  

@app.post("/remove/{itemId}")
def remove(itemId:int):        
    todos.delete(itemId)               

def body():
    return Body(Main(form_input(),Article(table()),cls="container"),htmx_script_tag())

def table():
    return Table(Thead(Tr(Th("Tasks",scope="col"))),Tbody(*[todo_row(todo) for todo in todos()],id="items_list"))

def todo_row(todo:Todo):
    return Tr(Td(Label(done_checkbox(todo.id,todo.done),todo.item,delete_button(todo.id)),scope="row"),cls="animate-slide-down",id=f'tr_{todo.id}')

def done_checkbox(id:int,done:bool):
    if(done==True):
        return Input(type="checkbox",name="itemId", value="yes", hx_post=f'/done/{id}', checked="true")
    else:
        return Input(type="checkbox", name="itemId", value="yes", hx_post=f'/done/{id}')

def form_input():
    return Form(Fieldset(Input(type="text",name="item",required="true",placeholder="Add Todo"),Button(submit_icon(),type="submit"),role="group"),hx_post="/",hx_target="#items_list",hx_swap="beforeend",hx_on_submit="this.reset()")

def submit_icon():
    return I("send",cls="material-icons")

def delete_button(id:int):
    return Button(I("delete",cls="material-icons"),cls="delete outline contrast pico-color-red-600",hx_post=f'/remove/{id}',hx_target=f'#tr_{id}',hx_swap="outerHTML")