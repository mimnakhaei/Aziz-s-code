from fastapi.security import OAuth2PasswordBearer
from typing import Optional
#from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta
from jose import jwt, JWTError
# from jose.exceptions import JWEError, JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import Depends, HTTPException, status
from db import db_users
 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = '648f906aab25618448e3b1a1a2278ca68ee81d4381217aa4b9ad949039b12ba5'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
    # expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
    # expire = datetime.now(timezone.utc) + timedelta(minutes=15)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db_users.get_user_by_username(db, username=username)
  
  if user is None:
    raise credentials_exception
  
  return user