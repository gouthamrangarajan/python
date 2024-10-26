import base64
from starlette.requests import *
from data.db import get_user_chat_sessions

def parse_cookie_and_get_user_id(request:Request):
    if("id" in request.cookies):
        return base64.b64decode(request.cookies.get("id").encode("utf8")).decode('utf-8') 
    return None
def parse_cookie_and_get_user_sessions(request:Request):
    user_id=parse_cookie_and_get_user_id(request)
    if(user_id is not None):  # check if user_id is in the cookie, if not return None
        user_id=base64.b64decode(request.cookies.get("id").encode("utf8")).decode('utf-8') 
        return get_user_chat_sessions(user_id)  
    return None