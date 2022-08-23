

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schema, utils


routers = APIRouter(
	prefix="/users",
	tags=['Users']
)

@routers.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_users(user:schema.UserCreate, db: Session = Depends(get_db)):

	# hash password
	hash_password = utils.hash(user.password)
	user.password = hash_password

	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit() 
	#Refresh
	db.refresh(new_user)

	return new_user

@routers.get("/{idx}", response_model=schema.UserOut)
def get_users(idx: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.idx == idx).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {idx} doesn't exist")

	return user