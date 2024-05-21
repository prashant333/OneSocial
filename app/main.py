from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# pydantic model for input validation. 
class Post(BaseModel):
    title: str
    content: str
    publish: bool = True #if user does not specify publish value, default will be true.

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

@app.get("/login")
async def root():
    return {"message": "Welcome to my new api!!!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"Connection successful"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def createpost(user_post: Post):
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""",
                   (user_post.title, user_post.content, user_post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    # post_data = user_post.dict()
    # post_data['id'] = randrange(0,100000)
    # my_post.append(post_data)
    return{"data": new_post}

@app.get("/post/{id}")
def get_posts(id: int, response:Response):
    cursor.execute("""select * from posts where id = %s""", (str(id)))
    post_data = cursor.fetchone()
    # user_post = find_post(id)
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'post with id: {id} was not found'}
    return {"data": post_data}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
    
    # my_post.pop(index)
    return{"message": f"Post with id: {id} was deleted succesfully"}

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    # index = find_index(id)
    cursor.execute("""update posts set title= %s, content = %s, published = %s where id= %s returning *""",
                   (post.title, post.content, post.publish, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    
    return{"data": f"Post with id: {id} was updated successfully "}