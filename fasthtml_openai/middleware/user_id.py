import base64
from datetime import datetime,timedelta, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import *
from starlette.responses import *
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
ENVIRONMENT=os.environ.get("ENVIRONMENT")


# Middleware that checks for a specific cookie
class UserIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Retrieve the cookie from the request
        id_cookie = request.cookies.get("id")
        
        response = await call_next(request)
        if request.url.path == "/": # do this only for first request
            if not id_cookie: 
                print(f'setting id in cookie')
                user_id_uuid=uuid.uuid4()
                user_id=base64.b64encode(str(user_id_uuid).encode('utf-8')).decode('utf-8')                
                expires_at = datetime.now(timezone.utc) + timedelta(days=400)  # Cookie expiry set for 400 days
                response.set_cookie("id",value=user_id,
                    httponly=True,samesite='strict',secure= ENVIRONMENT=='Production' if True else False,
                    expires=expires_at)
        return response           