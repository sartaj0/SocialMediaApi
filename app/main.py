from typing import List, Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from sqlalchemy.orm import Session
from . import utils

from . import models, schema
from .database import engine, get_db
from .data_manager import *

from . routers import post, user, auth
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