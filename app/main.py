from typing import Union, Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from random import randrange

from .data_manager import *

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str 
    publication: bool = True
    rating: Optional[int] = None


my_posts = MyPostDataBase()


@app.get("/")
def root():
    return {"message": "HelloWorld"}


@app.get("/posts")
def get_posts():
    return {'data': my_posts.posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1e+6)
    my_posts.store(post_dict)
    return {"data": post_dict}


@app.post("/temp")
def temp_test(post: dict=Body(...)):
    return {'message', 'temp tested Successfully'}


@app.get("/posts/{idx}")
def  get_post(idx: int, response: Response):
    post_detail = my_posts.find_post(idx)
    if post_detail is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'Post with id: {idx} was not found'}
        ## OR
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")
    return {"post_detail":post_detail}


## We dont return data/message when we delete
@app.delete("/posts/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(idx: int, response: Response):
    execution = my_posts.delete_post(idx)
    print(execution)
    if execution:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")


@app.put("/posts/{idx}")
def update_post(idx: int, post: Post):
    post_dict = post.dict()
    post_dict["id"] = idx
    execution = my_posts.update_post(idx, post_dict)
    print(execution)
    if execution:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")
    return {'message': "updated the post"}