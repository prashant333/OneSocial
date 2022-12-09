from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str

@app.get("/how")
async def root():
    return {"message": "Welcome to my new api"}

@app.get("/post")
def get_post():
    return {"data": "This is a sample post"}

@app.post("/create_post")
def createpost(new_post: Post):
    print("title: " +new_post.title)
    return{"data": "new_post created"}

