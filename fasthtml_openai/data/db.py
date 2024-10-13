from datetime import datetime
import os
from dotenv import load_dotenv
import libsql_experimental as libsql

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

conn = libsql.connect("local.db", sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
conn.sync()

def insert_user(id:str):
    conn.execute("INSERT INTO users (user_id, created_at) VALUES (?,?)",(id,datetime.now().timestamp()))
    conn.commit()
def get_user(id:str):
    return conn.execute("SELECT user_id FROM users WHERE user_id=?",(id,)).fetchone()
    
def insert_chat_session(user_id:str,title:str):
    cur=conn.cursor()
    cur.execute("INSERT INTO chat_sessions (user_id, title,created_at) VALUES (?,?,?)",(user_id,title,datetime.now().timestamp()))
    conn.commit()
    return cur.lastrowid

def get_user_chat_sessions(user_id:str):
    return conn.execute("SELECT session_id,title FROM chat_sessions WHERE user_id=?",(user_id,)).fetchall()

def get_first_user_chat_session(user_id:str):
    return conn.execute("SELECT session_id,title FROM chat_sessions WHERE user_id=?",(user_id,)).fetchone()

def get_user_chat_session(session_id:int,user_id:str):
    return conn.execute("SELECT session_id,title FROM chat_sessions WHERE session_id=? AND user_id=?",(session_id,user_id)).fetchone()

def get_user_chat_conversations(session_id:int):
    return conn.execute("SELECT message, sender FROM chat_conversations WHERE session_id=?",(session_id,)).fetchall()

def insert_chat_conversation(user_id:str,session_id:int, message:str, sender:str):      
    user=get_user(user_id)      
    if(user is None):
        insert_user(user_id)
    session=get_user_chat_session(session_id,user_id)
    if(session is None):
        session_id=insert_chat_session(user_id,message)
    conn.execute("INSERT INTO chat_conversations (session_id, message, sender, timestamp) VALUES (?,?,?,?)",(session_id,message,sender,datetime.now().timestamp()))
    conn.commit()
    return session_id