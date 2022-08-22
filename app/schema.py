from datetime import datetime
import typing
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
	title: str
	content: str 
	published: bool = True


class PostCreate(PostBase):
	pass 


class PostUpdate(PostBase):
	pass


class PostResponse(PostBase):
	title: str
	content: str
	published: bool
	# created_at: datetime

	class Config:
		orm_mode = True


class UserCreate(BaseModel):
	email: EmailStr
	password: str


class UserOut(BaseModel):
	idx: int 
	email: EmailStr
	created_at: datetime
	class Config:
		orm_mode = True

class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str 
	token_type: str 
	class Config:
		orm_mode = True

class TokenData(BaseModel):
	idx: Optional[str] = None 
