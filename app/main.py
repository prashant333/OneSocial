from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

@app.get("/post")
def get_posts():
    return {"data": my_post}

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def createpost(user_post: Post):
    post_data = user_post.dict()
    post_data['id'] = randrange(0,100000)
    my_post.append(post_data)
    return{"data": my_post}

@app.get("/posts/{id}")
def get_posts(id: str, response:Response):
    user_post = find_post(id)
    if not user_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'post with id: {id} was not found'}
    return {"data": user_post}

@app.delete("/posts/{id}")
def delete_post(id):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
        
    my_post.pop(index)
    return{"message": f"Post with id: {id} was deleted succesfully"}

@app.put("/posts/{id}")
def update_post(id, post:Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return{"data": f"Post with id: {id} was updated successfully "}