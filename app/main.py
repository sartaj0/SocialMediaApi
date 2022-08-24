from typing import List

from fastapi import FastAPI
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine

from . routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
	return {"message": "HelloWorld"}


@app.post("/temp")
def temp_test(post: dict=Body(...)):
	return {'message', 'temp tested Successfully'}