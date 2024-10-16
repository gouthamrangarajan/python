from fasthtml.common import *
from fasthtml.components import Zero_md
from data.db import get_first_user_chat_session, get_user_chat_conversations, get_user_chat_sessions, insert_chat_conversation
from data.user_chat_model import UserChat
from middleware.user_id import UserIdMiddleware
from openai_chat import chat
from mocks.javascript import mock_javascript_val
from mocks.python import mock_python_val 

app,rt = fast_app()
app.mount("/assets",StaticFiles(directory="assets"), name="assets")
app.add_middleware(UserIdMiddleware)

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
    return Script(src="/assets/library/alpine.min.js",type="text/javascript",defer=True)
def script_error_template():
    with open("./assets/error_template_assistant.js","r") as file:
        error_template_assistant= file.read()
    
    with open("./assets/error_template_user.js","r") as file:
        error_template_user= file.read()
    
    return (Script(f'{error_template_assistant}',type="text/template",id="errorTemplateAssistant"),
            Script(f'{error_template_user}',type="text/template",id="errorTemplateUser"))
def script_zero_md():
    # below does not work figure out why
    # return Script(src="/assets/library/zero-md.min.js",type="module") 
    return Script(src="https://cdn.jsdelivr.net/npm/zero-md@3?register",type="module")
def script_app():
    return Script(src="/assets/app.js",type="text/javascript")
def loader_span(cnt:int):
    if(cnt==1):
        return Span(cls=f'w-1.5 h-1.5 rounded-full animate-bounce-1 bg-white')
    elif(cnt==2):
        return Span(cls=f'w-1.5 h-1.5 rounded-full animate-bounce-2 bg-white')    
    return Span(cls=f'w-1.5 h-1.5 rounded-full animate-bounce-3 bg-white')
def loader():
    return Div(Img(src="/assets/openai.svg",cls="w-6 h-6 shrink-0")
              ,P(loader_span(1),loader_span(2),loader_span(3),cls="flex gap-1",style="view-transition-name:loader")              
              ,cls="flex gap-2 items-center w-full text-white p-1 htmx-indicator",id="loader")
def chat_container(conversations:list[dict]):
    conversation_els= [li_conversation(conversation) for conversation in conversations]
    user_conversation=list(filter(lambda el: el[1]=='user',conversations ))
    # adding empty li_assistant in the beginning so that array comes as input during post so the first index of assitant will always be ignored
    # adding empty li_user in the end so that it can be accessed by alpine to inject optimistic ui
    return Div(
        Ul(li_assistant(),*conversation_els,li_user(len(user_conversation)),id="list"),
        loader(),
        tabindex="0",id="scroll-div",
        cls="w-full border border-white rounded overflow-y-auto overflow-x-hidden scroll-smooth pb-20 h-[73vh] transition duration-300 scrollbar-thin scrollbar-track-gray-300 scrollbar-thumb-red-300 focus:ring-1 focus:ring-slate-300 focus:ring-offset-2 focus:ring-offset-slate-700 xl:h-[78vh]")
def li_conversation(conversation:dict):
    if(conversation[1]=="user"):
        return Li(I("person",cls="material-icons shrink-0"),P(conversation[0]),Input(type="hidden",name="user",value=f'{conversation[0]}'),
                cls="flex gap-2 items-start w-full text-white p-1"
              )
    else:
        return li_assistant(conversation[0],False)
              
def li_user(idx:int=0):
    return Li(I("person",cls="material-icons shrink-0"),P(x_text=f'$store.prompts.data[{idx}]'),Input(type="hidden",name="user",x_model=f'$store.prompts.data[{idx}]'),
              cls="flex gap-2 items-start w-full text-white p-1 animate-scale-y origin-top",
              x_show=f'$store.prompts.data[{idx}]!=""'
              )
def li_assistant(val:str="",animate:bool=True):
    if(val==""):
        return Li(P(val),Input(type="hidden",name="assistant",value=f'{val}'),cls=f'flex gap-2 items-start w-full text-white p-1 origin-top {"animate-scale-y" if animate else ""}')
    elif(val=="Error. Try again."):
        return Li(P(val),Input(type="hidden",name="assistant",value=''),cls=f'flex gap-2 items-start w-full text-white p-1 origin-top {"animate-scale-y" if animate else ""}')
    
    css_template = Template(Style('.markdown-body {background-color: rgb(30 41 59) !important; color: rgb(255 255 255) !important;}'), data_append=True)
    md_val=Zero_md(css_template, Script(val.replace("</script>","<\\/script>"), type="text/markdown"))
    # md_val=NotStr(f'''<zero-md><script type="text/markdown">{val}</script></zero-md>''')
    return Li(Img(src="/assets/openai.svg",cls="w-6 h-6 shrink-0"),
              P(md_val,cls=f'overflow-x-auto scrollbar-thin scrollbar-track-gray-300 scrollbar-thumb-red-300 origin-top {"animate-scale-y" if animate else ""}'),
              Input(type="hidden",name="assistant",value=f'{val}'),cls="flex gap-2 items-start w-full text-white p-1")    
def form(session_id:int,conversations:list[dict]):           
    return Form(h1(),chat_container(conversations),form_fields(),Input(id="sessionId",type="hidden",value=f'{session_id}',name="sessionId"),
                hx_trigger="chat_submit",
                hx_post="/message",hx_target="#list",hx_indicator="#loader",
                hx_swap="beforeend transition:true",hx_on_htmx_before_send="formBeforeSend(event,this)",
                hx_on_htmx_response_error="formError(event,this)",
                hx_on_htmx_before_swap="beforeSwap(event,this)",
                hx_on_htmx_after_swap="afterSwap(event,this)",
                x_cloak=True,
                cls="w-full mx-auto py-2 px-4 flex flex-col gap-6 items-center justify-center lg:w-7/12 xl:w-6/12 ")
def form_fields():
    return Div(
                input_field(),
                submit_btn(),
                cls="flex w-full appearance-none items-center gap-1 rounded border border-slate-300 bg-transparent px-4 py-2 text-white shadow outline-none transition duration-300  focus-within:ring-1 focus-within:ring-slate-300 focus-within:ring-offset-2 focus-within:ring-offset-slate-700"               
             )
def input_field():
    return Textarea(cls="flex-1 resize-none appearance-none bg-transparent outline-none scrollbar-thin scrollbar-track-transparent scrollbar-thumb-red-300 disabled:cursor-not-allowed disabled:opacity-60", 
                    name="prompt", placeholder="Send a message", id="txtMessage",rows="2",
                    x_model="$store.prompts.currentVal",
                    onKeyDown="keyDown(event,this)")        
def submit_btn():
    return Button(
            I("arrow_upward",cls="material-icons",x_show="!$store.processing.value"),
            Span(loader_span(1),loader_span(2),cls="flex gap-1",x_show="$store.processing.value"),
            type="submit",onClick="submitBtnClick(event,this)",            
            cls="appearance-none outline-none p-1 rounded-full bg-slate-700 text-white transition duration-300 disabled:cursor-not-allowed disabled:opacity-60 focus:ring-1 focus:ring-white")
def h1():
    return H1("Chat with OpenAI",cls="text-xl font-semibold text-red-300 lg:text-2xl")
@rt("/")
def get(request:Request):
    conversations=[]
    session_id=1
    if("id" in request.cookies):
        user_id=base64.b64decode(request.cookies.get("id").encode("utf8")).decode('utf-8') 
        session=get_first_user_chat_session(user_id)
        if(session is not None):
            session_id=session[0]
            conversations=get_user_chat_conversations(session_id)            
    return Html(
        Head(Title("Fasthtml OpenAI"),
        Meta(name="viewport",content="width=device-width, initial-scale=1.0"),
        Meta(name="description",content="Simple OpenAI chat using FastHTML"),
        fav_icon(),link_icons(),link_easings_css(),link_css()),
        Body(
            Main(form(session_id,conversations),cls="bg-slate-800 w-screen h-screen overflow-hidden",x_data="{}"),
            script_app(),    
            script_error_template(),       
            script_alpine(),            
            script_htmx(),
            script_zero_md()
        )
    )
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
    if(sessionId!=output_session_id):
        return li_assistant(f'{output}'),li_user(nxtDataIdx),Input(id="sessionId",type="hidden",value=f'{output_session_id}',hx_swap_oob="true",hx_swap="outerHTML")
    return li_assistant(f'{output}'),li_user(nxtDataIdx)

serve()
