
from sqlalchemy.orm import Session
from app import models, utils
from fastapi import Depends, APIRouter, status, HTTPException
from app.schemas import UserCreate, UserResponse
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def createUser(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{user_id}", response_model=UserResponse)
def getUser(user_id: int, db: Session = Depends(get_db)):
    currentUser = db.query(models.User).filter(models.User.id == user_id).first()

    if not currentUser:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"User with id: {user_id} does not exist")
    
    return currentUser