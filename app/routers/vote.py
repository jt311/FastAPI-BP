from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends, APIRouter, status, HTTPException
from app import oauth2, models
from app.schemas import VotePost

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def votePost(vote: VotePost, db: Session = Depends(get_db), currUserID: int = Depends(oauth2.getCurrentUser)):
    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == currUserID)
    voteFoundStatus = voteQuery.first()
    
    currentPost = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not currentPost:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {vote.post_id} does not exist")
    
    if vote.vote_direction == 1:
        if voteFoundStatus:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"User: {currUserID} has already voted for post with ID: {vote.post_id}")
        else:
            newVote = models.Vote(post_id = vote.post_id, user_id = currUserID)
            db.add(newVote)
            db.commit()
            
            return {"message": "Successfully added vote"}
    elif vote.vote_direction == 0:
        if not voteFoundStatus:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Post with ID: {vote.post_id} does not exist. Cannot vote")
        else:
            voteQuery.delete(synchronize_session=False)
            db.commit()

            return {"message": "Successfully deleted vote"}
