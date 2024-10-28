from fasthtml.common import *
from fasthtml.components import Zero_md

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
def form(session_id:int,conversations:list[dict]):           
    return Div(menu_button_and_h1(),
                Form(chat_container(conversations),form_fields(),input_session(session_id),
                hx_trigger="chat_submit",
                hx_post="/message",hx_target="#list",hx_indicator="#loader",
                hx_swap="beforeend transition:true",hx_on_htmx_before_send="formBeforeSend(event,this)",
                hx_on_htmx_response_error="formError(event,this)",                
                hx_on_htmx_after_swap="afterSwap(event,this)",                
                cls="w-full mx-auto py-2 px-4 flex flex-col gap-6 items-center justify-center lg:w-7/12 xl:w-6/12 "),
               cls="flex flex-col gap-2 items-center justify-center w-full")
def menu_button_and_h1():
    alpine_x_click={'x-on:click':'$store.showSessions.toggle()'}
    return Div(Button(I("menu",cls="material-icons"),type="button",**alpine_x_click,
               cls="appearance-none outline-none text-white shadow mt-1 p-1 transition duration-300 rounded-full focus:ring-1 focus:ring-white hover:opacity-80"),
               H1("Chat with OpenAI",cls="w-full text-xl font-semibold text-red-300 text-center lg:text-2xl"),
            cls="flex justify-between items-center w-full py-2 px-4")
def chat_container(conversations:list[dict]):
    conversation_els= [li_conversation(conversation) for conversation in conversations]
    user_conversation=list(filter(lambda el: el[1]=='user',conversations ))
    # adding empty li_assistant in the beginning so that array comes as input during post so the first index of assitant will always be ignored
    # adding empty li_user in the end so that it can be accessed by alpine to inject optimistic ui
    return Div(
        Ul(li_assistant(),*conversation_els,li_user(len(user_conversation)),id="list"),
        loader(),
        tabindex="0",id="scroll-div",
        cls="w-full border border-white rounded overflow-y-auto overflow-x-hidden scroll-smooth pb-20 h-[73vh] transition duration-300 scrollbar-thin scrollbar-track-gray-300 scrollbar-thumb-red-300 focus:ring-1 focus:ring-slate-300 focus:ring-offset-2 focus:ring-offset-slate-700 xl:h-[78vh]",
        style="view-transition-name:chat-container")
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
    
    css_template = Template(Style('.markdown-body {background-color: rgb(30 41 59) !important; color: rgb(255 255 255) !important;} @media(prefers-color-scheme: dark){.markdown-body table{color:rgb(255 255 255) !important;}}'), data_append=True)
    md_val=Zero_md(css_template, Script(val.replace("</script>","<\\/script>"), type="text/markdown"))
    # md_val=NotStr(f'''<zero-md><script type="text/markdown">{val}</script></zero-md>''')
    return Li(Img(src="/assets/openai.svg",cls="w-6 h-6 shrink-0"),
              P(md_val,cls=f'overflow-x-auto scrollbar-thin scrollbar-track-gray-300 scrollbar-thumb-red-300 origin-top {"animate-scale-y" if animate else ""}'),
              Input(type="hidden",name="assistant",value=f'{val}'),cls="flex gap-2 items-start w-full text-white p-1")    
            
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
def input_session(session_id:int,oob:bool=False):
    if(oob==True):
       return Input(id="sessionId",type="hidden",value=f'{session_id}',name="sessionId",hx_swap_oob="true",hx_swap="outerHTML",hx_target="#sessionId")    
    return Input(id="sessionId",type="hidden",value=f'{session_id}',name="sessionId")  
def submit_btn():
    return Button(
            I("arrow_upward",cls="material-icons",x_show="!$store.prompts.processing"),
            Span(loader_span(1),loader_span(2),cls="flex gap-1",x_show="$store.prompts.processing"),
            type="submit",onClick="submitBtnClick(event,this)",            
            cls="appearance-none outline-none p-1 rounded-full bg-slate-700 text-white transition duration-300 disabled:cursor-not-allowed disabled:opacity-60 focus:ring-1 focus:ring-white hover:opacity-80")
def sessions():
    alpine_animation_transition_bindings={}
    alpine_animation_transition_bindings['x-transition:enter']='transition ease-spring-1 duration-[600ms]'
    alpine_animation_transition_bindings['x-transition:enter-start']='opacity-0 transform -translate-x-full'
    alpine_animation_transition_bindings['x-transition:enter-end']='opacity-1 transform translate-x-0'
    alpine_animation_transition_bindings['x-transition:leave']='transition ease-in-out-1 duration-300'
    alpine_animation_transition_bindings['x-transition:leave-start']='opacity-1 transform translate-x-0'
    alpine_animation_transition_bindings['x-transition:leave-end']='opacity-0 transform -translate-x-full'
    
    alpine_background_transition_bindings={}
    alpine_background_transition_bindings['x-transition:enter']='transition ease-in-out-1 duration-300'
    alpine_background_transition_bindings['x-transition:enter-start']='opacity-0'
    alpine_background_transition_bindings['x-transition:enter-end']='opacity-1'
    alpine_background_transition_bindings['x-transition:leave']='transition ease-in-out-1 duration-300'
    alpine_background_transition_bindings['x-transition:leave-start']='opacity-1'
    alpine_background_transition_bindings['x-transition:leave-end']='opacity-0'
    
    alpine_close_button_click_bindings={'x-on:click':'$store.showSessions.toggle()'}
    return Div(Div(Ul(Li(add_new_chat_button()),id="menu",hx_get="/sessions",hx_swap="beforeend",hx_trigger="load",cls="flex flex-col gap-1 items-center"),session_errors(),                
                cls="relative bg-slate-800 w-11/12 h-screen overflow-y-auto scrollbar-thin scrollbar-track-gray-300 scrollbar-thumb-red-300  py-2 px-4 pt-10 lg:w-1/3",
                id="menuContainer",style="view-transition-name:sessions",**alpine_animation_transition_bindings,x_show="$store.showSessions.value",),
               Button(I("close",cls="material-icons"),cls="outline-none appearance-none text-red-600 p-1 rounded-full transition duration-300 mt-2 focus:ring-1 focus:ring-red-600 hover:opacity-80",
               **alpine_close_button_click_bindings),
            cls="absolute flex gap-1 items-start bg-black/50 w-screen h-screen text-white z-10",style="view-transition-name:session-menu-open-background",
            **alpine_background_transition_bindings,x_show="$store.showSessions.value",x_trap="$store.showSessions.value")
def add_new_chat_button():               
    return Div(Button( Span(loader_span(1),loader_span(2),cls="flex gap-1 mr-1",x_show="processing"),
                    I("add",cls="material-icons",x_show="!processing"),Span("New Chat"),hx_post="/chat/new",hx_target="#menu",hx_swap="beforeend",hx_trigger="chat_new",hx_on_htmx_response_error="addNewChatError(event,this)",
                onClick="addChatClick(event,this)",cls="appearance-none outline-none cursor-pointer flex gap-1 items-center bg-slate-700 text-white py-2 px-4 rounded transition duration-300 focus:ring-1 focus:ring-white hover:opacity-80",
                x_data="{processing:false}")
            ,cls="pb-8")
def li_session(session:dict,oob:bool=False):
    if(oob):
        return Li(A(session[1],href=f'/{session[0]}',onClick="goToSession(event,this)",style=f'view-transition-name:session-title-{session[0]}',
                  cls="appearance-none outline-none transition duration-300 truncate text-ellipsis flex-1 p-1 rounded focus:ring-1 focus:ring-white hover:opacity-80"),
                session_title_edit_button(session),id=f'sessionLink_{session[0]}',
                cls="sessionLink border-b border-slate-600 w-full py-1 px-3 text-white flex items-center",
                hx_swap_oob="true",hx_target=f'#sessionLink_{session[0]}',hx_swap="outerHTML",               
                hx_on_htmx_after_swap=f'afterTitleEditSwap(event,this)',x_data="{processing:false}")
    return Li(A(session[1],href=f'/{session[0]}',onClick="goToSession(event,this)",style=f'view-transition-name:session-title-{session[0]}',
              cls="appearance-none outline-none transition duration-300 truncate text-ellipsis flex-1 p-1 rounded focus:ring-1 focus:ring-white hover:opacity-80"),
            session_title_edit_button(session), id=f'sessionLink_{session[0]}',
            cls="sessionLink border-b border-slate-600 w-full py-1 px-3 text-white flex items-center",           
            hx_on_htmx_after_swap=f'afterTitleEditSwap(event,this)',x_data="{processing:false}")
def session_title_edit_button(session:dict):
    alpine_click_binding={'x-on:click':'processing=true'}
    return  Button(I("edit",cls="material-icons",x_show="!processing"),
                   Span(loader_span(1),loader_span(2),cls="flex gap-1",x_show="processing"),
           cls="outline-none appearance-none text-white p-1 rounded-full transition duration-300  flex gap-1 items-center focus:ring-1 focus:ring-white hover:opacity-80",
           style=f'view-transition-name:session-title-action-{session[0]}', 
           hx_get=f'/{session[0]}/edit/title',hx_target="closest li",hx_swap="innerHTML transition:true",
           hx_on_htmx_response_error="titleEditError(event,this)",
           **alpine_click_binding,      
           )
def first_li_session(session:dict):
    return Ul(li_session(session),
            hx_swap_oob="beforeend:#menu")
def form_edit_session_title(session:dict):
    alpine_submit_binding={'x-on:submit':'processing=true'}
    return Form(Input(type="text",value=f'{session[1]}',name="title",
                 cls="apperance-none outline-none bg-transparent py-1 px-3 rounded-lg border border-white transition duration-300 text-white flex-1",
                 style=f'view-transition-name:session-title-{session[0]}'),
                 Button(I('check',cls="material-icons",x_show="!processing"),
                        Span(loader_span(1),loader_span(2),cls="flex gap-1",x_show="processing"),
                 type="submit",style=f'view-transition-name:session-title-action-{session[0]}',
                 cls="outline-none appearance-none text-white p-1 rounded-full transition duration-300  focus:ring-1 focus:ring-white hover:opacity-80"),
            cls="flex items-center flex-1 gap-1",hx_post=f'/{session[0]}/edit/title',hx_target="closest li",
            hx_swap="outerHTML transition:true",hx_on_htmx_response_error="titleEditError(event,this)",
            **alpine_submit_binding
                )
def session_errors():
    alpine_bindings_template_key={}
    alpine_bindings_template_key['x-bind:key']='error.id'
    alpine_bindings_list_style={}
    alpine_bindings_list_style['x-bind:style']='{"view-transition-name":"error-msg-"+error.id}'
    alpine_bindings_remove_click={}
    alpine_bindings_remove_click['x-on:click']='$store.errors.remove(error.id)'
    templates=Template(Li(Span(x_text="error.msg",cls="flex-1"),
                          Button("CLEAR",
                          cls="outline-none appearance-none text-xs text-slate-600 bg-red-50 p-1 transition duration-300 focus:ring-1 focus:ring-red-50 focus:ring-offset-1 focus:ring-offset-red-600 hover:opacity-80",
                          **alpine_bindings_remove_click),
                        cls="bg-red-600 text-white rounded py-1 px-3 flex gap-2 items-center animate-error-msg",
                        **alpine_bindings_list_style),
               x_for="error in $store.errors.value",**alpine_bindings_template_key)
    return Ul(templates,x_show="$store.errors.value.length>0", cls="absolute bottom-2 left-2 w-11/12 mx-auto items-center flex flex-col gap-1")