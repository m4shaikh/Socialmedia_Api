from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import model, schema, Oauth2
from ..database import get_db
from sqlalchemy.orm import joinedload
router=APIRouter(
    prefix="/post"
)

#get all posts

@router.get('/',response_model=List[schema.PostOut])
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(Oauth2.get_user)):
    posts = db.query(model.Post).all()
    return posts

#get posts by id

@router.get('/{id}',response_model=schema.PostOut)
def get_post_byid(id:int , db:Session = Depends(get_db), current_user: int = Depends(Oauth2.get_user)):
    
    Post = db.query(model.Post).filter(model.Post.id == id).first()

    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found") 
    print(Post)
    return {"Post": Post}
    
#create post

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_post(post:schema.PostCreate, db:Session = Depends(get_db),current_user:int=Depends(Oauth2.get_user)):
    print(current_user.id)
    new_post = model.Post(owner_id = current_user.id , **post.dict())
   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return "post created successfully"