from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# pydantic model for input validation. 
class Post(BaseModel):
    title: str
    content: str
    publish: bool = True #if user does not specify publish value, default will be true.
    rating: Optional[int] = None

@app.get("/login")
async def root():
    return {"message": "Welcome to my new api!!!"}

@app.get("/post")
def get_post():
    return {"data": "This is a sample post"}

@app.post("/create_post")
def createpost(user_post: Post):
    print(user_post.rating)
    # printing the pydantic instance into dictionary
    print(user_post.dict())
    return{"data": user_post}

