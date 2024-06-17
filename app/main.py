from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models, schema, utils
from database import engine, get_db
from router import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', 
        password = 'thisisnewPassword#', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connection to databasea failed")
        print("Error:", error)
        time.sleep(4)

my_post = [{"titile": "title 1", "content":"content 1", "publish":"True", "id":"1"},
           {"titile": "title 2", "content":"content 2", "publish":"False", "id":"2"}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)