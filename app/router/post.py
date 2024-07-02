from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
import models, schema, oauth2
from database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


""" this is testing endpoint using ORM module sqlalchemy """

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status":posts}

@router.get("/", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def createpost(user_post: schema.PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""",
    #                (user_post.title, user_post.content, user_post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    # post_data = user_post.dict()
    # post_data['id'] = randrange(0,100000)
    # my_post.append(post_data)

    new_post = models.Post(**user_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=List[schema.PostResponse])
def get_posts(id: int, response:Response, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id = %s""", (str(id)))
    # post_data = cursor.fetchone()
    # # user_post = find_post(id)
    # if not post_data:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'post with id: {id} was not found')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f'post with id: {id} was not found'}

    post_data = db.query(models.Post).filter(models.Post.id == id).first()
    return post_data

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
    post.delete(synchronize_session=False)
    db.commit()

    return{"message": f"Post with id: {id} was deleted succesfully"}

@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: int, post:schema.PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # index = find_index(id)
    # cursor.execute("""update posts set title= %s, content = %s, published = %s where id= %s returning *""",
    #                (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_1 = post_query.first()
    if post_1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    
    return{"data": f"Post with id: {id} was updated successfully "}
