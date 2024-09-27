import base64
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import *
from starlette.responses import *
from starlette.exceptions import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
USER_ID=os.environ.get("USER_ID")


# Middleware that checks for a specific cookie
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Retrieve the cookie from the request
        id_cookie = request.cookies.get("id")
        
        print(f"checking {request.url.path} in middleware")                
        
        skip_starts_with_paths=['/assets/']
        for path in skip_starts_with_paths:
            if request.url.path.startswith(path):
                response = await call_next(request)
                return response
        
        cookie_present=True
        if not id_cookie: 
            cookie_present=False
        else:
            decodedCookie = base64.b64decode(id_cookie.encode('utf-8')).decode('utf-8')
            if decodedCookie!=USER_ID:
                cookie_present=False
                           
        if request.url.path.lower()=="/login":
            if cookie_present == True:                
                return RedirectResponse("/")
        # Check the cookie value for authentication
        else:
            if cookie_present == False:
                print(f'UnAuthorized')
                return RedirectResponse("/login")
        
        # Call the next middleware or endpoint
        response = await call_next(request)
        return response