
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db
from app import oauth2

router = APIRouter(prefix="/votes", tags=["Vote"])

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_vote(vote: schemas.VoteIn, get_current_user = Depends(oauth2.get_current_user),db: Session = Depends(get_db)):
    if(vote.vote_dir == 1):
        new_vote = models.Vote(post_id = vote.post_id, user_id= get_current_user.id, )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
    else:
        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id)
        vote = vote_query.first()

        if(vote == None):
            utils.raise_404(f"post with id {vote.post_id} not found")

        vote_query.delete(synchronize_session=False)
        db.commit()

    


