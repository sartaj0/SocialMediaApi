from typing import Union, Optional

from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from random import randrange

from store import *

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


@app.post('/posts')
def create_posts(post: Post):

    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1e+6)
    print(post_dict)
    my_posts.store(post_dict)
    return {"data": post_dict}


@app.post("/temp")
def temp_test(post: dict=Body(...)):
    print(post)
    return {'message', 'temp tested Successfully'}