from pickletools import read_uint1
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
# secret key
# algorithm
# Expiration key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encode_jwt


def verify_acces_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		idx: str = payload.get("user_id")
		if idx is None:
			raise credentials_exception
		token_data = schema.TokenData(idx=idx)
	except JWTError:
		raise credentials_exception
	return token_data


def get_current_user(token: str= Depends(oauth2_scheme)):
	credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"www-authenticate": "Bearer"})
	return verify_acces_token(token, credentials_exception)



