from fastapi import FastAPI,Depends
from .router import post,user,login,votes
from sqlalchemy.orm import Session
from .database import get_db,engine
from . import model
app=FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def geto(db:Session=Depends(get_db)):
    
    return "hello"

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(votes.router)