from typing import List, Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from sqlalchemy.orm import Session

from . import models, schema
from .database import engine, get_db
from .data_manager import *


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# my_posts = MyPostDataBase()


@app.get("/")
def root():
	return {"message": "HelloWorld"}


@app.get("/posts", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db)):
	# posts = my_posts.get_posts()
	posts = db.query(models.Post).all()
	return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED,  response_model=schema.PostResponse)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
	# post_dict = post.dict()
	# new_post = my_posts.store(post_dict)

	# new_post = models.Post(title=post.title, content=post.content, published=post.published)
	new_post = models.Post(**post.dict())
	db.add(new_post)
	db.commit() 
	
	#Refresh
	db.refresh(new_post)
	return new_post


@app.post("/temp")
def temp_test(post: dict=Body(...)):
	return {'message', 'temp tested Successfully'}


@app.get("/posts/{idx}", response_model=schema.PostResponse)
def get_post(idx: int, db: Session = Depends(get_db)):
	# post_detail = my_posts.find_post(idx)
	post = db.query(models.Post).filter(models.Post.idx == idx).first()
	
	if post is None:
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"message": f'Post with id: {idx} was not found'}
		## OR
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")
	return post


## We dont return data/message when we delete
@app.delete("/posts/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(idx: int, db: Session = Depends(get_db)):
	# execution = my_posts.delete_post(idx)
	post = db.query(models.Post).filter(models.Post.idx == idx)
	if post.first() != None:
		post.delete(synchronize_session=False)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")


@app.put("/posts/{idx}", response_model=schema.PostResponse)
def update_post(idx: int, post: schema.PostCreate, db: Session = Depends(get_db)):
	# post_dict = post.dict()
	# post_dict["id"] = idx
	# execution = my_posts.update_post(idx, post_dict)
	post_query = db.query(models.Post).filter(models.Post.idx == idx)
	if post_query.first() != None:
		post_query.update(post.dict(), synchronize_session=False)
		db.commit()
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idx} was not found")


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_users(user:schema.UserCreate, db: Session = Depends(get_db)):
	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit() 
	#Refresh
	db.refresh(new_user)

	return new_user

