from typing import Union, Optional

from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
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
    print(post)
    print(post.dict())
    return {"message", "Successfully created post"}


@app.post("/temp")
def temp_test(post: dict=Body(...)):
    print(post)
    return {'message', 'temp tested Successfully'}