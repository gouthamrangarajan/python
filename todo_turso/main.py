import bcrypt
from fasthtml.common import *
from data.libsql import delete_task, get_all_tasks, add_task, mark_task_completed
from middlewares.auth import AuthMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
PWD_HASH= os.environ.get("PWD_HASH")
ENVIRONMENT= os.environ.get("ENVIRONMENT")
USER_ID=os.environ.get("USER_ID")

app,rt = fast_app()
app.mount("/assets",StaticFiles(directory="assets"), name="assets")
app.add_middleware(AuthMiddleware)

def easings_link():
    return Link("",rel="stylesheet",href="https://unpkg.com/open-props/easings.min.css")

def icons_link():
    return Link("",rel="stylesheet",href="https://fonts.googleapis.com/icon?family=Material+Icons")

def app_css_link():
    return Link("",rel="stylesheet",href="/assets/app.css")

def head():
    return Head(Title("ToDo Turso"),icons_link(),easings_link(),app_css_link(),Meta(name="viewport",content="width=device-width, initial-scale=1.0"))

def htmx_script():
    return Script(src="/assets/htmx.min.js",type="text/javascript")

def login_page_script():
    return Script(src="/assets/login.js",type="text/javascript")

def todo_page_script():
    return Script(src="/assets/todo.js",type="text/javascript")

def login_container():    
    return Form(login_input(),id="loginForm",
                cls="flex flex-col gap-1 bg-white py-2 px-4 shadow-2xl shadow-green-500/50 w-full max-w-xl mx-auto rounded-xl animate-login",
                style=f'view-transition-name:login-form',   
                hx_post="/login",hx_trigger="login",hx_target="#error",hx_swap="outerHTML transition:true",
                hx_on_htmx_after_swap="loginRedirect()",hx_on_htmx_before_request="disableForm()",
                hx_on_htmx_after_request="enableForm()")

def login_input():
    return (Label("Enter Password",cls="text-slate-600 font-semibold"),
            Input(name="password",type="password",
                onKeyDown="pwdKeyDown(event,this)",                 
                cls="appearance-none outline-none py-1 px-3 rounded border-2 border-slate-600 transition duration-300 focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 focus:ring-offset-slate-50",
                 style=f'view-transition-name:login-input'),
            Div(id="error",style=f'view-transition-name:login-error'),
            Button("Login",id="loginBtn",
                cls="w-full bg-slate-600 text-white transition duration-300 py-1 px-3 rounded focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 focus:ring-offset-slate-50",
                onClick="loginButtonClick(event,this)",
                style=f'view-transition-name:login-button'),            
            )

def add_task_input():
    return Input(type="text", placeholder="Add a new task", name="task",id="inp_add",
                onKeyDown="textKeyDown(event,this)",
                hx_trigger="add_submit",hx_post="/", hx_target="#list",hx_swap="beforeend",
                cls="appearance-none outline-none py-1 px-3 rounded-xl border-2 border-slate-600 transition duration-300 focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 focus:ring-offset-slate-50")

def container():
    tasks = get_all_tasks()
    tasks_lis= [task_li(task) for task in tasks]
    return Div(add_task_input(),Ul(*tasks_lis,cls="h-[80vh] overflow-y-scroll scroll-pr-1 w-full flex flex-col gap-1",id="list"),cls="flex flex-col gap-2 shadow-2xl shadow-green-500/50 w-full max-w-xl mx-auto rounded-xl")

def task_completed_checkbox(data):    
    if(data[2]==1):
        return Input(type="checkbox",cls="appearance-none outline-none w-5 h-5 rounded-full border-2 border-slate-600 focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 focus:ring-offset-slate-50",
                     checked=true, hx_trigger="change", hx_post=f"/complete/{data[0]}",hx_target=f'#span_{data[0]}',hx_swap="outerHTML")
    else:
        return Input(type="checkbox",cls="appearance-none outline-none w-5 h-5 rounded-full border-2 border-slate-600 focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 focus:ring-offset-slate-50",
                     hx_trigger="change", hx_post=f"/complete/{data[0]}",hx_target=f'#span_{data[0]}',hx_swap="outerHTML")
    
def task_label(data):    
    return Label(task_completed_checkbox(data),check_icon_span(data),Span(data[1],cls="flex-1 break-all"),cls="has-[:checked]:line-through flex flex-1 items-center gap-3 relative")
    
def task_li(data):
    return Li(task_label(data),remove_button(data),cls="border-b w-full border-b-slate-300 py-1 px-3 animate-list flex items-center gap-1",id=f'li_{data[0]}',style=f'view-transition-name:list-{data[0]}')

def check_icon_span(data):
    if(data[2]==1):
        return Span(I('check',cls="material-icons text-xl"),cls="absolute -top-0.25 left-0 -z-10 animate-opacity",id=f'span_{data[0]}')
    else:
        return Span('',cls="absolute top-0 left-0 -z-10 animate-opacity",id=f'span_{data[0]}')
    
def remove_button(data):
    return Button(I('delete',cls="material-icons text-xl"),cls="appearance-none outline-none py-1 px-2 rounded border border-red-600 text-red-600 transition duration-300 focus:ring-2 focus:ring-red-600 focus:ring-offset-2 focus:ring-offset-red-50",
                 onClick="removeBtnClick(event,this)",
                 hx_trigger="remove_submit",hx_post=f'/delete/{data[0]}',hx_target=f'#li_{data[0]}',hx_swap="delete transition:true")

@rt("/login")
def get():
    return Html(head(),Body(Main(login_container(),cls="h-screen w-screen flex p-1 items-center flex-col justify-center"),login_page_script(),htmx_script()))     

@rt("/login")
def post(password:str):           
    # hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # print(hash.decode('utf-8'))
    verify=bcrypt.checkpw(password.encode('utf-8'), PWD_HASH.encode('utf-8'))
    if verify:
        response=Response(content='<div id="error" style="view-transition-name:login-error"></div>')
        response.set_cookie(key="id", value=base64.b64encode(USER_ID.encode('utf-8')).decode('utf-8'),httponly=True,samesite='strict',
                            secure= ENVIRONMENT=='Production' if True else False)
        return response
    return Div("Please enter valid password",id="error",cls="font-semibold animate-list w-full text-red-600",style=f'view-transition-name:login-error')
        
@rt("/")
def get():        
    return Html(head(),Body(Main(container(),cls="h-screen w-screen flex p-1 pt-10 flex-col justify-center"),todo_page_script(),htmx_script()))

@rt("/")
def post(task:str):  
    new_data=(add_task(task),task,0)  
    return task_li(new_data)

@rt("/complete/{task_id}")
def post(task_id:int):
    data=mark_task_completed(task_id)
    return check_icon_span(data)

@rt("/delete/{task_id}")
def post(task_id:int):
    delete_task(task_id)
    return None
    
serve()