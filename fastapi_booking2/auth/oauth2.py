from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWEError, JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import Depends, HTTPException, status
from db import db_users
 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = 'b943d9d0956b7c311046f38d30936b06ffc02407a1395a5189bb44bd34207138'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    # expire = datetime.utcnow() + expires_delta  --> replaced with blow line
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    
    # expire = datetime.utcnow() + timedelta(minutes=15)--> replaced with blow line
      expire = datetime.now(timezone.utc) + timedelta(minutes=15)

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
  except JWEError:
    raise credentials_exception
  
  user = db_users.get_user_by_username(db, username)
  
  if user is None:
    raise credentials_exception
  
  return user