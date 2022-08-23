from typing import List

from fastapi import FastAPI
from fastapi.params import Body

from . import models
from .database import engine

from . routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# my_posts = MyPostDataBase()


app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.router)

@app.get("/")
def root():
	return {"message": "HelloWorld"}


@app.post("/temp")
def temp_test(post: dict=Body(...)):
	return {'message', 'temp tested Successfully'}