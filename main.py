from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/how")
async def root():
    return {"message": "Welcome to my new api"}

@app.get("/post")
def get_post():
    return {"data": "This is a sample post"}

@app.post("/create_post")
def createpost(payLoad: dict = Body(...)):
    print(payLoad)
    return{"new_post": f"title :{payLoad['title']} content: {payLoad['content']}"}