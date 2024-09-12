
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db
from app import oauth2

router = APIRouter(prefix="/votes", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteIn, get_current_user = Depends(oauth2.get_current_user),db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == get_current_user.id)
    
    found_vote = vote_query.first()
    
    if(vote.vote_dir == 1):
        if(post == None):
            utils.raise_404(f"post with id {vote.post_id} not found")

        if found_vote:
            utils.raise_409(f"user {get_current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id= get_current_user.id)
        
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
        
    else:
        
        if(found_vote == None):
            utils.raise_404(f"post with id {vote.post_id} not found")

        vote_query.delete(synchronize_session=False)
        
        db.commit()
        
        return {"message": "successfully unvoted a post"}

    


