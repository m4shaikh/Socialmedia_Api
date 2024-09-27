from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schema, Oauth2, database ,model


from sqlalchemy.orm import Session
router = APIRouter(
    prefix='/vote'
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote, db:Session=Depends(database.get_db), current_user:int = Depends(Oauth2.get_user)):
    
    vote_query = db.query(model.Votes).filter(model.Votes.post_id == vote.post_id , model.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted ")
        new_vote = model.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"Message":"you have successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not voted")
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return{"Message":"your vote is successfuly deleted"} 