import os
from dotenv import load_dotenv
import libsql_experimental as libsql

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL","libsql://general-gouthamrangarajan.turso.io")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN","eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MjY3ODg4MjUsImlkIjoiZjQ3MjU0NjItODVjMi00MWQyLWE0YWMtZDkzNjdmODk4ZjMxIn0.5zJf4PcP0qAW2DRHEBH277sSeDxBHdxMrnubb3ByqC_EmK_EGTlDsqZZStraaEofkRtjoSzqTyjnV59aZB-yCg")

conn = libsql.connect("general.db", sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
conn.sync()

def get_all_tasks():
    return conn.execute("select * from tasks").fetchall()

def add_task(description: str):
    cursor=conn.cursor()
    cursor.execute("insert into tasks (description) VALUES (?)", (description,))
    conn.commit()
    return cursor.lastrowid

def mark_task_completed(task_id: int):
    data=conn.execute("select * from tasks where id = ?", (task_id,)).fetchone()
    completed=1
    if(data[2]==0):
        conn.execute("update tasks set completed=1 where id=?", (task_id,))
    else:
        conn.execute("update tasks set completed=0 where id=?", (task_id,))
        completed=0
    conn.commit()
    ret_data=(task_id,data[1],completed)
    return ret_data

def delete_task(task_id:int):
    conn.execute("delete from tasks where id=?", (task_id,))
    conn.commit()