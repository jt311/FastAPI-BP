
from sqlalchemy.orm import Session
from app import models, oauth2
from fastapi import Depends, APIRouter, status, HTTPException, Response
from app.schemas import PostBase, PostResponse, PostOutput
from app.database import get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=list[PostOutput], dependencies=[Depends(oauth2.getCurrentUser)])
def read_root(db: Session = Depends(get_db), qpLimit: int = 10, qpSkip: int = 0, qpSearch: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(qpSearch)).limit(qpLimit).offset(qpSkip).all()
    
    return posts

@router.get("/{item_id}", response_model=PostOutput, dependencies=[Depends(oauth2.getCurrentUser)])
def read_item(item_id: int, db: Session = Depends(get_db)):
    currentPost = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
        models.Post.id == item_id).first()

    if not currentPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {item_id} does not exist")

    return currentPost

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def createPost(post: PostBase, db: Session = Depends(get_db), currUserID: int = Depends(oauth2.getCurrentUser)):
    newPost = models.Post(user_id = currUserID, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@router.delete("/{id}")
def deletePost(id: int, db: Session = Depends(get_db), currUserID: int = Depends(oauth2.getCurrentUser)):
    currentPostQuery = db.query(models.Post).filter(models.Post.id == id)
    currentPost = currentPostQuery.first()

    if not currentPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist")
    
    if currentPost.user_id != currUserID:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorised to delete post"
        )
    
    currentPostQuery.delete(synchronize_session=False)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def updatePost(id: int, post: PostBase, db: Session = Depends(get_db), currUserID: int = Depends(oauth2.getCurrentUser)):
    currentPostQuery = db.query(models.Post).filter(models.Post.id == id)
    currentPost = currentPostQuery.first()

    if not currentPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist")
    
    if currentPost.user_id != currUserID:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorised to update post")

    currentPostQuery.update(values = post.dict())
    db.commit()
    return currentPost 