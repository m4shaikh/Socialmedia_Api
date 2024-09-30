from fastapi import APIRouter, Depends, HTTPExeption, status
from sqlalchemy.orm import Session
from .. import schema,model,utils
from ..database import get_db


router = APIRouter(
    prefix="/user"
)

@router.post('')
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = model.User(**user.dict())
    db.add(new_user) 
    db.commit()

    return "post created successfully "

@router.get('/{id}',response_model=schema.UserOut)
def get_user(id:int , db:Session = Depends(get_db)):
    
    user = db.query(model.User).filter(model.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exists")
    
    return user
