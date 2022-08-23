from typing import List

from fastapi import FastAPI
from fastapi.params import Body

from . import models
from .database import engine

from . routers import post, user, auth
from pydantic import BaseSettings

class Setting(BaseSettings):
	database_password: str = "localhost"
	database_username: str = "sqlite3"
	secret_key: str = "1234567890"

setting = Setting()


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