from sqlalchemy.orm import Session
from datetime import timedelta
from app import models, utils, oauth2
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas import Token
from app.database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=Token)
def loginUser(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    currentUser = db.query(models.User).filter(models.User.email == userCredentials.username).first()

    if not currentUser or not utils.verify(userCredentials.password, currentUser.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Email or Password")
    
    accessToken = oauth2.createAccessToken(
        data = {"user_id": currentUser.id},
        expireDelta = timedelta(minutes = oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": accessToken,
        "token_type": "bearer"
        }

    