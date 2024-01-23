from jose import jwt, JWTError
from datetime import datetime, timedelta
from schemas import TokenData
from database import get_db
from models import User
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dontuploadcredentials import secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email:str = payload.get("user_email")
        if email is None:
            raise credentials_exception
        id:int = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(user_email=email, user_id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token.user_email).first()

    if user is None:
        raise credentials_exception

    return user