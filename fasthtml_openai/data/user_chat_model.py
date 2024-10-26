from pydantic import BaseModel


class UserChat(BaseModel):    
    sessionId:int
    prompt:str
    user:list[str]=[]
    assistant:list[str]=[]
    
    def to_tuple(self):
        return (self.sessionId, self.prompt, self.user, self.assistant)        