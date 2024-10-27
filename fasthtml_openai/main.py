from fasthtml.common import *
from data.db import get_first_user_chat_session, get_user_chat_conversations, insert_chat_conversation, insert_chat_session, update_chat_session_title
from data.user_chat_model import UserChat
from main_helper import parse_cookie_and_get_user_id, parse_cookie_and_get_user_sessions
from main_ui_controls import *
from middleware.no_cache import NoCacheMiddleware
from middleware.user_id import UserIdMiddleware
from openai_chat import chat
from mocks.javascript import mock_javascript_val
from mocks.python import mock_python_val 

app,rt = fast_app()
app.mount("/assets",StaticFiles(directory="assets"), name="assets")
app.add_middleware(UserIdMiddleware)
app.add_middleware(NoCacheMiddleware)

def link_easings_css():
    return Link(href="/assets/library/easings.min.css",rel="stylesheet")

def link_css():
    return Link(href="/assets/app.css",rel="stylesheet")

def fav_icon():
    return Link(href="/assets/favicon.ico",rel="icon")

def link_icons():
    return Link(href="/assets/library/material-icons.css",rel="stylesheet")

def script_htmx():
    return Script(src="/assets/library/htmx.min.js",type="text/javascript")

def script_alpine():
    return (Script(src="/assets/library/alpine-focus.min.js",type="text/javascript",defer=True),
            Script(src="/assets/library/alpine.min.js",type="text/javascript",defer=True))
    
def script_error_template():
    with open("./assets/error_template_assistant.js","r") as file:
        error_template_assistant= file.read()
    
    with open("./assets/error_template_user.js","r") as file:
        error_template_user= file.read()
    
    return (Script(f'{error_template_assistant}',type="text/template",id="errorTemplateAssistant"),
            Script(f'{error_template_user}',type="text/template",id="errorTemplateUser"))
    
def script_zero_md():
    # below does not work figure out why
    return Script(src="/assets/library/zero-md.min.js?register",type="module") 
    # return Script(src="https://cdn.jsdelivr.net/npm/zero-md@3?register",type="module")

def script_app():
    return Script(src="/assets/app.js",type="text/javascript")
            
@rt('/sessions')
def get(request:Request):    
    sessions= parse_cookie_and_get_user_sessions(request)
    if(sessions is not None):        
        sessions_li=[li_session(session) for session in sessions]
        return sessions_li
    return None

@rt("/{session_id}/edit/title")
def get(request:Request,session_id:int=0):
    all_sessions=parse_cookie_and_get_user_sessions(request)
    if(all_sessions is not None):        
        if(session_id!=0):
            all_sessions_filter=list(filter(lambda dt:dt[0]==session_id,all_sessions))
            if(len(all_sessions_filter)>0):
                return form_edit_session_title(all_sessions_filter[0])
    return Response("UnAuthorized",status_code=401)

@rt("/{session_id}/edit/title")
def post(request:Request,session_id:int,title:str):     
    all_sessions=parse_cookie_and_get_user_sessions(request)   
    if(all_sessions is not None):        
        if(session_id!=0):
            all_sessions_filter=list(filter(lambda dt:dt[0]==session_id,all_sessions))
            if(len(all_sessions_filter)>0):
                session=all_sessions_filter[0]                
                if(len(title.strip())>0):
                    update_chat_session_title(session_id,title)
                    session=(session[0],title)
                return li_session(session)
    return Response("UnAuthorized",status_code=401)

@rt("/{session_id}")
def get(request:Request,session_id:int=0):
    conversations=[]    
    all_sessions=parse_cookie_and_get_user_sessions(request)
    user_id= parse_cookie_and_get_user_id(request)
    if(user_id is not None):        
        session=get_first_user_chat_session(user_id)        
        if(session_id!=0):
            all_sessions_filter=list(filter(lambda dt:dt[0]==session_id,all_sessions))
            if(len(all_sessions_filter)==0):
                return Response("UnAuthorized",status_code=401)
        if(session is not None):
            if(session_id==0):
                session_id=session[0]
            conversations=get_user_chat_conversations(session_id)            
    return Html(
        Head(Title("Fasthtml OpenAI"),
        Meta(name="viewport",content="width=device-width, initial-scale=1.0"),
        Meta(name="description",content="Simple OpenAI chat using FastHTML"),
        fav_icon(),link_icons(),link_easings_css(),link_css()),
        Body(
            Main(sessions(),form(session_id,conversations)
                 ,cls="relative w-screen h-screen overflow-hidden",x_data="{}",x_cloak=True),
            script_app(),    
            script_error_template(),       
            script_alpine(),            
            script_htmx(),
            script_zero_md(),
            cls="bg-slate-800"
        )
    )
    
@rt('/chat/new')
def post(request:Request):
    if("id" in request.cookies):
        user_id=base64.b64decode(request.cookies.get("id").encode("utf8")).decode('utf-8') 
        new_session_id=insert_chat_session(user_id,'New Chat')
        dict={}
        dict[0]=new_session_id
        dict[1]='New Chat'
        return (Input(id="sessionId",type="hidden",value=f'{new_session_id}',name="sessionId",hx_swap_oob="true",hx_target="#sessionId",hx_swap="outerHTML"),li_session(dict))
    return None

@rt("/message")
async def post(request:Request,user_chat:UserChat):    
    sessionId,prompt,user,assistant=user_chat.to_tuple()
    user_id=base64.b64decode(request.cookies.get("id").encode("utf8")).decode('utf-8')    
    output_session_id=insert_chat_conversation(user_id,sessionId,prompt,"user")
    # last item in user array is empty
    # first item in assistant array is empty
    nxtDataIdx=len(user)
    if(nxtDataIdx==0):
        nxtDataIdx=1
    if(len(user)==0):
        user.append(prompt)        
    else:
        user[len(user)-1]=prompt
    messages=[]   
    for index,item in enumerate(user):
        messages.append({"role":"user","content":item})
        if(index+1<len(assistant)):
            messages.append({"role":"assistant","content":assistant[index+1]})    
    output=await chat(messages) 
    # output=mock_python_val   
    # output=mock_javascript_val    
    output_session_id=insert_chat_conversation(user_id,output_session_id,output,"assistant")
    out_els=[]
    if(len(messages)==1):
        update_chat_session_title(output_session_id,prompt[0:50]) 
        dict={}
        dict[0]=output_session_id
        dict[1]=prompt
        if(sessionId!=output_session_id):            
            out_els.append(first_li_session(dict))   
        else:
            out_els.append(li_session(dict,true))
    if(sessionId!=output_session_id):        
        out_els.append(input_session(output_session_id,True))        
    out_els.append(li_assistant(f'{output}'))
    out_els.append(li_user(nxtDataIdx))    
    return out_els

serve()
