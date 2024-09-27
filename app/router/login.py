from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schema, model, Oauth2
from ..database import get_db
from ..Oauth2 import create_token

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def log_in(user_creds:OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):
    
    user = db.query(model.User).filter(model.User.email == user_creds.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    access_token = Oauth2.create_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}