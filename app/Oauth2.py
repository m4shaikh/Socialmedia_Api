from jose import jwt,JWTError
from datetime import datetime, timedelta
from . import schema, database, model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

secret_key = settings.secret_key
algo = settings.algorithm
exp_time = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):

    toencode = data.copy()
    toencode.update({"exp":datetime.utcnow()+timedelta(minutes=exp_time)})
    encoded_token = jwt.encode(toencode, secret_key, algorithm=algo)
    return encoded_token 

def verify_token(token:str , exceptions):
  
    try:

        payload = jwt.decode(token, secret_key, algorithms=[algo])
        id: str = payload.get("user_id")
        if id is None:
            raise exceptions
        token_data = schema.TokenData(id=str(id))

        print(token_data.dict())
    except JWTError:
        raise exceptions
    
    return token_data


def get_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token_data = verify_token(token, credentials_exception)
    print(token_data.id)
    user = db.query(model.User).filter(model.User.id == token_data.id).first()
    
    return user