from fastapi import FastAPI
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine
from router import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#code for connecting database and using raw sql
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', 
#         password = 'thisisnewPassword#', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("Connection to databasea failed")
#         print("Error:", error)
#         time.sleep(4)

        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)